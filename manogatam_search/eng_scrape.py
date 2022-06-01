import requests
import re
from bs4 import BeautifulSoup as bsoup
import os
import asyncio
import aiohttp
import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

date_list = set()
for _file in os.listdir("."):
    if _file.endswith(('.txt', '.pdf')):
        date_list.add(_file[:-4])


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r.content


def gsoup(url):
    return bsoup(get_html(url), 'html.parser')


def fetch_all_urls():
    pages_url = 'https://www.pmindia.gov.in/wp-admin/admin-ajax.php?action=demoMannKiBaat&page_no={no}&language=en&tag=mann-ki-baat'
    i = 0
    res = []
    while True:
        adds = gsoup(pages_url.format(no=i)).find_all(
            "a", href=re.compile(r'(-address-in-|-mann-ki-)'))
        if not adds:
            break
        for add in adds:
            res.append(add["href"])
        i += 1
    return res


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


def parse(wd, html, url):
    add_soup = bsoup(html, 'html.parser')
    pdt = add_soup.find("span", attrs={'class': 'date'}).text
    if datetime.datetime.strptime(pdt, '%d %b, %Y').strftime('%Y-%m-%d') not in date_list:
        return
    res = []
    for para in (add_soup.find_all("p")):
        for sent_txt in para.text.split("."):
            if bool(re.search(wd, sent_txt)):
                cres = (sent_txt, url)
                if cres:
                    res.append(cres)
    return res


async def scrape_urls(wd, urls):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *(fetch_and_parse(wd, session, url) for url in urls)
        )


async def fetch_and_parse(wd, session, url):
    html = await fetch(session, url)
    loop = asyncio.get_event_loop()
    # run parse(html) in a separate thread, and
    # resume this coroutine when it completes
    paras = await loop.run_in_executor(None, parse, wd, html, url)
    return paras


def get_res(wd):
    loop = asyncio.get_event_loop()
    group = scrape_urls(wd, fetch_all_urls())
    results = loop.run_until_complete(group)
    loop.close()
    return [res for res in results if res]


if __name__ == '__main__':
    import sys
    print(get_res(sys.argv[1]))

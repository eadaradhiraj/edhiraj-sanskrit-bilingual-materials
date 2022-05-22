urld = {
    "math": {
        "10": "jemh1",
        "9": "iemh1"
    },
    "science": {
        "9": "iesc1",
        "10": "jesc1"
    },
    "economics": {
        "10": "jess2",
        "9": "iess2"
    },
    "history": {
        "10": "jess3",
        "9": "iess3"
    },
    "civics": {
        "10": "jess4",
        "9": "iess4"
    },
    "geography": {
        "10": "jess1",
        "9": "iess1"
    }
}


def geturl(fname, subj, stand):
    print(subj, stand, f"https://ncert.nic.in/ncerts/l/{urld[subj][stand]}{fname}.pdf" )

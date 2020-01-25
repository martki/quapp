"""
> Et bilde tar mer lagringsplass enn tusen ord

Links:
- https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/nowiki/20191220/
- https://dumps.wikimedia.org/enwiki/
- https://docs.google.com/document/d/1Z4RriWnRApEfLA_aJZFT2PlxvYXTFoNUwBtfEDycnAw/edit
"""

LINKS = [
    "https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/nowiki/20191220/nowiki-20191220-pages-articles.xml.bz2",
]


# import ftplib

# ftp = ftplib.FTP("https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/nowiki/20191220")

# status = ftp.login()

import requests

url = "https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/nowiki/20191220/nowiki-20191220-change_tag_def.sql.gz"

r = requests.get(url)

print(r)

input(1111)

#import antigravity
import bz2

file_name = "data/nowiki-20191220-pages-articles.xml.bz2"

with bz2.open(file_name, mode="rt", encoding="utf-8") as zf:
    title = False
    for i, line in enumerate(zf):
        if title:
            print(line[11:-9])
            title = not title
        if line == "  <page>\n":
            title = not title

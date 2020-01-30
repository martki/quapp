"""
> Et bilde tar mer lagringsplass enn tusen ord

Links:
- https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/nowiki/20191220/
- https://dumps.wikimedia.org/enwiki/
- https://docs.google.com/document/d/1Z4RriWnRApEfLA_aJZFT2PlxvYXTFoNUwBtfEDycnAw/edit

Wikitext/wikicode
https://en.wikipedia.org/wiki/Help:Wikitext
"""

#import antigravity
import bz2
import re
from itertools import dropwhile, takewhile

concatenate = " ".join

re_title = r'<title>(?P<title>.*?)</title>'

re_text = r'<text xml:space="preserve">(?P<text>.*?)' + "(?:" + "|".join(f"==\s?{title}\s?==" for title in ["Bilder", "Se også", "Noter", "Referanser", "Bibliografi", "Litteratur", "Eksterne lenker"]) + "|</text>)"


# Does not recognize <sub> and <sup>, nor nested {{}}

wikicode = {
    r'\{\|.*?\|\}' : '',
    r'\{\{.*?\}\}' : '',
    # Remove square bracket around links:
    # [[Øyeren]] --> Øyeren
    r'\[\[(?P<text>[^\|]*?)\]\]': r'\g<text>',
    # Remove and replace links with alt names
    # [[Fil:Oyern1.jpg|thumb|[[Elv|Elvedelta]]et i [[Øyeren]]]]
    # --> [[Fil:Oyern1.jpg|thumb|Elvedeltaet i Øyeren]]
    r'\[\[[^:]+?\|(?P<alt>.*?)\]\]': r'\g<alt>',
    # Remove and replace media files
    # [[Fil:Oyern1.jpg|thumb|Elvedeltaet i Øyeren]]
    # (Bilde av Elvedeltaet i Øyeren)
    r'\[\[\w+?:[^\]]*\|(?P<alt>.*?)\]\]': r'(Bilde av \g<alt>) ',
    r"(?P<quotes>'+?)(?P<formatted>.*?)(?P=quotes)": r"\g<formatted>",
    r"&lt;ref.*?&gt;.*?&lt;/ref&gt;": "",
    r"&lt;ref.*?/&gt;": "",
    r"&lt;gallery.*?&gt;.*?&lt;/gallery&gt;": "",
    # titles
    r"(?P<equals>=+?)(?P<title>.*?)(?P=equals)": r"\n\g<title>\n",
    # remove comments
    r"&lt;!--.*?--&gt;": "",
    r"&amp;" : "&",
    r"&nbsp;" : " ",
    r"&quot;" : '"',
}

file_name = "data/nowiki-20200101-pages-articles.xml.bz2"

# s = """[[File:Castle of Aggerhus (JW Edy plate 53).jpg|thumb|GGAkershus festning i 1800; festningen lå da i sentrum av både GGAkershus amt som tilsvarte de sentrale delene av den moderne GGOsloregionen og GGAkershus stiftamt som i hovedsak tilsvarte GGØstlandet]]"""
#
# s = re.search(r'\[\[\w+?:[^\]]*\|(?P<alt>.*?)\]\]', s)
# input(s)
# input(s["alt"])

# s = re.sub(r'\[\[\w+?:(?:^]*?)\|(?P<alt>.*?)\]\]', r'\g<alt>', s)
# input(s)

with bz2.open(file_name, mode="rt", encoding="utf-8") as zf:
    zf = map(str.strip, zf)
    while 1:
        page = dropwhile(lambda l: l != "<page>", zf)
        page = takewhile(lambda l: l != "</page>", page)

        # filter empty strings
        page = concatenate(filter(None, page))

        title = re.search(re_title, page)["title"]

        text = re.search(re_text, page)["text"]

        # print(text)


        for expr, sub in wikicode.items():
            text = re.sub(expr, sub, text)

        print(f"""
=== {title} ===

{text}
""")
        input("Press any key to view next article")

    # title = False
    # for i, line in enumerate(zf):
    #     print(line, end="")
    #     if title:
    #         input(line[11:-9])
    #         title = not title
    #     if line == "  <page>\n":
    #         title = not title

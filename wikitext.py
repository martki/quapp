"""
> Et bilde tar mer lagringsplass enn tusen ord

Links:
- https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/nowiki/20191220/
- https://dumps.wikimedia.org/enwiki/

Wikitext/wikicode
https://en.wikipedia.org/wiki/Help:Wikitext
"""

#import antigravity
import bz2
import re
from itertools import dropwhile, takewhile
from textwrap import dedent

concatenate = " ".join

re_title = re.compile(r'<title>(?P<title>.*?)</title>')

re_text = re.compile(r'<text xml:space="preserve">(?P<text>.*?)' + "(?:" + "|".join(f"==\s?{title}\s?==" for title in ["Bilder", "Se også", "Noter", "Referanser", "Bibliografi", "Litteratur", "Eksterne lenker"]) + "|</text>)")

# substitution patterns (applied in order)
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

# compile expressions for minor speedup
wikicode = {
    re.compile(expr) : sub for expr, sub in wikicode.items()
}


def wikireader(file_name):
    with bz2.open(file_name, mode="rt", encoding="utf-8") as zf:
        zf = map(str.strip, zf)
        while 1:
            # Does not include closing tag, but it is not needed
            page = dropwhile(lambda l: l != "<page>", zf)
            page = takewhile(lambda l: l != "</page>", page)

            # filter empty strings
            page = concatenate(filter(None, page))

            if not page: break

            title = re_title.search(page)["title"]
            text = re_text.search(page)["text"]

            for expr, sub in wikicode.items():
                text = expr.sub(sub, text)

            yield title, text



if __name__ == "__main__":
    file_name = "data/nowiki-20200101-pages-articles.xml.bz2"

    for title, text in wikireader(file_name):
        print(dedent(f"""
        === {title} ===

        {text}
        """))

        input("Press any key to view next article")

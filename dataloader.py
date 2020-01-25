from pathlib import Path
import pandas
import requests
import bz2
from ftplib import FTP

# main directory where all data will be saved
DATA_DIR = 'data/'

urls = [
    "https://acc.umu.se/mirror/wikimedia.org/dumps/nowiki/20200102/nowiki-20200101-pages-articles.xml.bz2", 
]


def fetch_data(url):
    try:
        """
        r_obj = requests.get(url)
        print(r_obj.status_code)
        """
        ftp_obj = FTP("ftp:acc.umu.se/mirror/wikimedia.org/dumps/nowiki/20200101/")
        print(ftp_obj)
    except: 
        print(f'error')
        


def load_wikipedia(data):
    pass


def fetch_all():
    for url in urls:
        fetch_data(url)

if __name__ == "__main__":
   fetch_all() 
     
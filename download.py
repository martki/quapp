from pathlib import Path
import requests
import shutil

# inspiration:
# https://github.com/openai/gpt-2-output-dataset/blob/master/download_dataset.py

# directory where all data will be saved
DATA_DIR = Path("data/")

# Remember to add a comma after each entry!
urls = [
    "http://ftp.acc.umu.se/mirror/wikimedia.org/dumps/nowiki/20200101/nowiki-20200101-pages-articles.xml.bz2",
]


### ========================================================= ###


def download_file(url, filename, *, dir=DATA_DIR):
    with requests.get(url, stream=True) as r:
        with open(DATA_DIR / filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return filename



def downloaded_files():
    return set(path.name for path in DATA_DIR.iterdir())



def fetch_uninstalled_data():
    downloads = downloaded_files()
    for url in urls:
        _base_url, filename = url.rsplit("/", maxsplit=1)

        if filename in downloads:
            print(f"Skipping installed file {filename}")
            continue

        print(f"Fetching content from {url}")
        download_file(url, filename)
        print(f"Finished installing {filename} to {DATA_DIR}")



if __name__ == "__main__":
    fetch_uninstalled_data()

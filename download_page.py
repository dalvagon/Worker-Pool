import os
import urllib.request
from bs4 import BeautifulSoup


def download_page(url, location):
    if not os.path.exists(location):
        os.mkdir(location)

    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read(), features="html.parser")

    try:
        with open(os.path.join(location, f"file.html"), "w", encoding="utf-8") as file:
            file.write(soup.prettify())
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    url = "http://youtube.com"
    location = "saveFiles"
    download_page(url, location)

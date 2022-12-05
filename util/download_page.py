import os
import logging
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from util.colors import MAGENTA, BLUE, CYAN, GREEN, YELLOW, RED, ENDC, BOLD, UNDERLINE


def download_page(url, location):
    """
    Download a page from the address specified by url in the directory specified by the location

    :param url: The link to the page to be doenloaded
    :param location: the path to the directory where the page will be downloaded
    """
    try:
        # response = request.urlopen(url)

        # soup = BeautifulSoup(response.read(), features="html.parser")

        # if not os.path.exists(location):
        #     os.makedirs(location)
        # with open(os.path.join(location, f"file.html"), "w", encoding="utf-8") as file:
        #     file.write(soup.prettify())

        with open(url, "r", encoding="utf8") as file:
            content = file.read()
            print(BOLD + GREEN + content + ENDC)
    except HTTPError:
        logging.error(
            RED
            + BOLD
            + "Page "
            + ENDC
            + YELLOW
            + UNDERLINE
            + url
            + ENDC
            + RED
            + BOLD
            + " not found"
            + ENDC
        )
    except Exception as e:
        logging.error(RED + BOLD + str(e) + ENDC)

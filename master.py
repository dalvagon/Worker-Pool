import json
import os
import logging
import pika
from util.get_countries import get_countries
from util.colors import MAGENTA, BLUE, CYAN, GREEN, YELLOW, RED, ENDC, BOLD, UNDERLINE

CONNECTION_STRING = "sites_queue"


def create_queue():
    """Creates the queue by pushing page links and the page download locations onto it"""
    logging.info(MAGENTA + BOLD + "Creating connection for queue..." + ENDC)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_delete(queue=CONNECTION_STRING)
    channel.queue_declare(queue=CONNECTION_STRING)

    logging.info(GREEN + BOLD + "Connection created" + ENDC)

    countries = get_countries()
    countries.sort()
    for country in countries:
        country_name = country.replace(" ", "")
        url = f"https://www.infoplease.com/countries/{country_name}"
        location = os.path.join(".", "pages", f"{country_name}")
        logging.info(
            MAGENTA
            + BOLD
            + "Pushing "
            + ENDC
            + CYAN
            + UNDERLINE
            + url
            + ENDC
            + MAGENTA
            + BOLD
            + " onto the queue. The page will be downloaded in "
            + ENDC
            + BLUE
            + UNDERLINE
            + location
            + ENDC
        )

        message = {
            "url": url,
            "location": location,
        }

        channel.basic_publish(
            exchange="", routing_key=CONNECTION_STRING, body=json.dumps(message)
        )

    connection.close()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    try:
        create_queue()
    except KeyboardInterrupt:
        logging.error(MAGENTA + BOLD + "Interrupted" + ENDC)
    except Exception as e:
        logging.error(str(e))

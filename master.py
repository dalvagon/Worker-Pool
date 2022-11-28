import os
import logging
import pika
from get_countries import get_countries
from colors import MAGENTA, BLUE, CYAN, GREEN, YELLOW, RED, ENDC, BOLD, UNDERLINE

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
    for country in countries:
        url = f"google.com/{country}"
        location = os.path.join(".", f"{country}")
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
            + " onto the queue. The page witll be downloaded in "
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
            exchange="", routing_key=CONNECTION_STRING, body=str(message)
        )

    connection.close()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    create_queue()

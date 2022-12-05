import json
import os
import logging
import pika
from util.get_countries import get_countries
from util.colors import MAGENTA, BLUE, CYAN, GREEN, YELLOW, RED, ENDC, BOLD, UNDERLINE

CONNECTION_STRING = "sites_queue"


def create_queue():
    """Create the queue by pushing page links and the page download locations onto it"""
    logging.info(MAGENTA + BOLD + "Creating connection for queue..." + ENDC)

    credentials = pika.PlainCredentials("dalvagon", "dalvagon")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_delete(queue=CONNECTION_STRING)
    channel.queue_declare(queue=CONNECTION_STRING)

    logging.info(GREEN + BOLD + "Connection created" + ENDC)
    for root, dirs, files in os.walk(os.path.join(".", "pages"), topdown=False):
        for file in files:
            url = os.path.join(root, file)
            location = os.path.join(".", "pagess", file)
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

    # countries = get_countries()
    # countries.sort()
    # for country in countries:
    #     country_name = country.replace(" ", "")
    #     url = f"https://www.infoplease.com/countries/{country_name}"
    #     location = os.path.join(".", "pages", f"{country_name}")
    #     logging.info(
    #         MAGENTA
    #         + BOLD
    #         + "Pushing "
    #         + ENDC
    #         + CYAN
    #         + UNDERLINE
    #         + url
    #         + ENDC
    #         + MAGENTA
    #         + BOLD
    #         + " onto the queue. The page will be downloaded in "
    #         + ENDC
    #         + BLUE
    #         + UNDERLINE
    #         + location
    #         + ENDC
    #     )

    #     message = {
    #         "url": url,
    #         "location": location,
    #     }

    #     channel.basic_publish(
    #         exchange="", routing_key=CONNECTION_STRING, body=json.dumps(message)
    #     )

    connection.close()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    try:
        create_queue()
    except KeyboardInterrupt:
        logging.error(RED + BOLD + "Interrupted" + ENDC)
    except Exception as e:
        logging.error(RED + BOLD + str(e) + ENDC)

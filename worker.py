import pika
import json
import logging
from util.colors import MAGENTA, BLUE, CYAN, GREEN, YELLOW, RED, ENDC, BOLD, UNDERLINE
from util.download_page import download_page

CONNECTION_STRING = "sites_queue"


def handle_message(ch, method, properties, body):
    """Handle a mesaage from the queue"""
    message = json.loads(body)
    logging.info(
        MAGENTA + BOLD + "Received message : " + ENDC + CYAN + str(message) + ENDC
    )
    download_page(message["url"], message["location"])
    ch.basic_ack(delivery_tag=method.delivery_tag)
    logging.info(MAGENTA + BOLD + "Finished processing the message\n" + ENDC)


def consume():
    """Consume the messages pushed by the master onto the queue"""
    logging.info(MAGENTA + BOLD + "Connecting..." + ENDC)

    credentials = pika.PlainCredentials("dalvagon", "dalvagon")
    parameters = pika.ConnectionParameters("localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue=CONNECTION_STRING)
    channel.basic_qos(prefetch_count=1)

    logging.info(GREEN + BOLD + "Connection established" + ENDC)

    logging.info(GREEN + BOLD + "Started consuming..." + ENDC)

    channel.basic_consume(queue=CONNECTION_STRING, on_message_callback=handle_message)
    channel.start_consuming()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    try:
        consume()
    except KeyboardInterrupt:
        logging.error(RED + BOLD + "Interrupted" + ENDC)
    except Exception as e:
        logging.error(str(e))

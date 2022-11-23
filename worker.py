import pika
import time
import random
import json


def handle_message(ch, method, properties, body):
    message = json.loads(body.decode("UTF8").replace("'", '"'))
    print(message["url"])
    processing_time = random.randint(1, 10)
    print(
        f"Received message: {message} will take {processing_time} seconds to complete"
    )
    time.sleep(processing_time)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Finished processing the message {message}")


def consume():
    CONNECTION_STRING = "sites_queue"

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=CONNECTION_STRING)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=CONNECTION_STRING, on_message_callback=handle_message)

    channel.start_consuming()


if __name__ == "__main__":
    consume()

import pika


def main():
    CONNECTION_STRING = "sites_queue"

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_delete(queue=CONNECTION_STRING)
    channel.queue_declare(queue=CONNECTION_STRING)

    count = 0
    while True:
        message = {"url": f"google.com/{count}", "location": "."}
        channel.basic_publish(
            exchange="", routing_key=CONNECTION_STRING, body=str(message)
        )
        count += 1

    connection.close()


if __name__ == "__main__":
    main()

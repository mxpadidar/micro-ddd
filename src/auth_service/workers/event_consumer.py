import json

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

RABBITMQ_HOST: str = "localhost"
RABBITMQ_DEFAULT_USER: str = "guest"
RABBITMQ_DEFAULT_PASS: str = "guest"


def callback(ch, method, properties, body):
    # Convert the body from bytes to string
    body_str = body.decode()

    # Parse the JSON string to a dictionary
    message = json.loads(body_str)

    # Handle the message
    # This could be anything you want to do with the message
    print(f"Received message: {message}")


def consume_event():
    # Connect to the RabbitMQ server
    connection = BlockingConnection(
        parameters=ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS),
        )
    )

    # Create a new channel
    channel = connection.channel()

    # Declare the queue
    queue = "events"
    channel.queue_declare(queue=queue)

    # Start consuming messages
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    consume_event()

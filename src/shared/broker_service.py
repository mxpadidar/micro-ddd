import json
from abc import ABC, abstractmethod

from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from shared.logger import Logger

logger = Logger("Message Broker Service")


class BrokerService(ABC):

    @abstractmethod
    def publish_message(self, exchange: str, routing_key: str, message: dict): ...

    @abstractmethod
    def consume_message(self, queue: str, callback): ...


class RabbitMQService(BrokerService):
    def __init__(self, host: str, user: str, password: str):
        self.connection = BlockingConnection(
            parameters=ConnectionParameters(
                host=host, credentials=PlainCredentials(user, password)
            )
        )
        self.channel = self.connection.channel()
        self.setup_queue(exchange="events", queue="events", routing_key="*")

    def publish_message(self, exchange: str, routing_key: str, message: dict):
        self.channel.exchange_declare(exchange=exchange, exchange_type="topic")

        message_ = json.dumps(message)
        self.channel.basic_publish(
            exchange=exchange, routing_key=routing_key, body=message_
        )
        logger.info(
            f"Message delivered to exchange {exchange} with routing key {routing_key}"
        )

    def consume_message(self, queue: str, callback):
        self.channel.queue_declare(queue=queue)

        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True
        )
        logger.info(f"Started consuming messages from queue {queue}")
        self.channel.start_consuming()

    def setup_queue(self, exchange: str, queue: str, routing_key: str):
        # Declare the exchange
        self.channel.exchange_declare(exchange=exchange, exchange_type="topic")

        # Declare the queue
        self.channel.queue_declare(queue=queue)

        # Bind the queue to the exchange with the routing key
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

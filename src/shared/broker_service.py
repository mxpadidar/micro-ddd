import json
from abc import ABC, abstractmethod

import pika

from shared.logger import Logger

logger = Logger("Message Broker Service")


class BrokerService(ABC):
    @abstractmethod
    def publish_message(self, exchange: str, routing_key: str, message: dict):
        pass

    @abstractmethod
    def consume_message(self, queue: str, callback):
        pass


class RabbitMQService(BrokerService):
    def __init__(self, host: str):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

    def publish_message(self, exchange: str, routing_key: str, message: dict):
        self.channel.exchange_declare(exchange=exchange, exchange_type="topic")

        message_ = json.dumps(message)
        self.channel.basic_publish(
            exchange=exchange, routing_key=routing_key, body=message_
        )
        logger.info(
            f"Published message {message} to exchange {exchange} with routing key {routing_key}"
        )

    def consume_message(self, queue: str, callback):
        self.channel.queue_declare(queue=queue)

        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True
        )
        logger.info(f"Started consuming messages from queue {queue}")
        self.channel.start_consuming()

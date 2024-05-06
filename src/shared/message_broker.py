import json
from abc import ABC, abstractmethod

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from redis import Redis


class MessageBroker(ABC):
    @abstractmethod
    def publish(self, destination: str, message: dict) -> None:
        """Publish a message to a destination."""

    @abstractmethod
    def subscribe(self, destination: str) -> None:
        """Subscribe to a destination."""

    @abstractmethod
    def get_message(self) -> dict | None:
        """Get the next message from the destination."""


class RedisMessageBroker(MessageBroker):
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        self.client = Redis(host=host, port=port, db=db)
        self.pubsub = self.client.pubsub()

    def publish(self, destination: str, message: dict) -> None:
        self.client.publish(destination, json.dumps(message))

    def get_message(self) -> dict | None:
        message = self.pubsub.get_message()
        if message and message["type"] == "message":
            return json.loads(message["data"])
        else:
            return None

    def subscribe(self, destination: str) -> None:
        self.pubsub.subscribe(destination)


class RabbitMQMessageBroker(MessageBroker):
    def __init__(self, host="localhost", user="guest", password="guest"):
        self.connection = BlockingConnection(
            parameters=ConnectionParameters(
                host=host, credentials=PlainCredentials(user, password)
            )
        )
        self.channel = self.connection.channel()
        self.destination = None

    def publish(self, destination: str, message: dict) -> None:
        self.channel.basic_publish(
            exchange="", routing_key=destination, body=json.dumps(message)
        )

    def subscribe(self, destination: str) -> None:
        self.channel.queue_declare(queue=destination)
        self.destination = destination

    def get_message(self) -> dict | None:
        method_frame, header_frame, body = self.channel.basic_get(
            queue=self.destination
        )
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            return None

from shared.base import BaseUnitOfWork, Command, Event
from shared.logger import Logger
from shared.message_broker import MessageBroker

logger = Logger("Message Bus")


class MessageBus:
    _queue: list[Command | Event]
    _response: dict | None = None

    def __init__(
        self, uow: BaseUnitOfWork, message_broker: MessageBroker, command_handlers: dict
    ):
        self.uow = uow
        self.message_broker = message_broker
        self.command_handlers = command_handlers

    def handle(self, message: Command | Event):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Command):
                self._handle_command(message)
            if isinstance(message, Event):
                self._handle_event(message)
        return self.response

    def _handle_event(self, event: Event):
        logger.info(event.__class__.__name__)
        self.message_broker.publish("events", event.to_dict())

    def _handle_command(self, command: Command):
        handler = self.command_handlers[type(command)]
        self.response = handler(command)
        new_events = self.uow.collect_new_events()
        self.queue.extend(new_events)

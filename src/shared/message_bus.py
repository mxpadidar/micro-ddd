from shared.base import BaseCommand, BaseEvent, BaseQuery, BaseUnitOfWork
from shared.broker_service import BrokerService
from shared.logger import Logger

logger = Logger("Message Bus")


class MessageBus:
    _queue: list[BaseCommand | BaseQuery | BaseEvent]
    _response: dict | None = None

    def __init__(
        self,
        uow: BaseUnitOfWork,
        broker_service: BrokerService,
        command_handlers: dict,
        query_handlers: dict,
    ):
        self.uow = uow
        self.broker_service = broker_service
        self.command_handlers = command_handlers
        self.query_handlers = query_handlers

    def handle(self, message: BaseCommand | BaseQuery | BaseEvent):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, BaseCommand):
                self._handle_command(message)
            if isinstance(message, BaseQuery):
                self._handle_query(message)
            if isinstance(message, BaseEvent):
                self._handle_event(message)

        return self.response

    def _handle_event(self, event: BaseEvent):
        # Serialize the event to a JSON string
        event_json = event.to_dict()

        # Define the exchange and routing key
        exchange = "events"
        routing_key = event.__class__.__name__

        # Publish the event
        self.broker_service.publish_message(exchange, routing_key, event_json)

    def _handle_command(self, command: BaseCommand):
        handler = self.command_handlers[type(command)]
        self.response = handler(command)
        new_events = self.uow.collect_new_events()
        self.queue.extend(new_events)

    def _handle_query(self, query: BaseQuery):
        handler = self.query_handlers[type(query)]
        return handler(query)

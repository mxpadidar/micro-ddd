from shared.base import BaseCommand, BaseQuery, BaseUnitOfWork


class MessageBus:
    def __init__(
        self, uow: BaseUnitOfWork, command_handlers: dict, query_handlers: dict
    ):
        self.uow = uow
        self.command_handlers = command_handlers
        self.query_handlers = query_handlers

    def handle(self, message: BaseCommand | BaseQuery):
        if isinstance(message, BaseCommand):
            return self._handle_command(message)
        if isinstance(message, BaseQuery):
            return self._handle_query(message)

    def _handle_command(self, command: BaseCommand):
        handler = self.command_handlers[type(command)]
        return handler(command)

    def _handle_query(self, query: BaseQuery):
        handler = self.query_handlers[type(query)]
        return handler(query)

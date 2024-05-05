from product.adapters.orm.mapper import start_mappers
from product.adapters.unit_of_work_impl import UnitOfWorkImpl
from product.service_layer.command_handlers import command_handlers_mapper
from product.service_layer.container import Container
from product.service_layer.query_handlers import query_handlers_mapper
from shared.auth_service import AuthService
from shared.message_broker import MessageBroker, RedisMessageBroker
from shared.message_bus import MessageBus
from shared.settings import REDIS_DB, REDIS_HOST, REDIS_PORT, STORAGE_SERVICE_URL
from shared.storage_service import StorageService
from shared.utils import inject_dependencies

start_mappers()


uow = UnitOfWorkImpl()


message_broker: MessageBroker = RedisMessageBroker(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB
)

auth_service = AuthService()

storage_service = StorageService(STORAGE_SERVICE_URL)


container = Container(
    uow=uow,
    storage_service=storage_service,
    message_broker=message_broker,
    auth_service=auth_service,
)


DEPENDENCIES = {
    "uow": uow,
    "message_broker": message_broker,
    "auth_service": auth_service,
    "storage_service": storage_service,
}


INJECTED_COMMAND_HANDLERS = {
    command_type: inject_dependencies(handler, DEPENDENCIES)
    for command_type, handler in command_handlers_mapper.items()
}

INJECTED_QUERY_HANDLERS = {
    query_type: inject_dependencies(handler, DEPENDENCIES)
    for query_type, handler in query_handlers_mapper.items()
}


bus = MessageBus(
    uow=UnitOfWorkImpl(),
    message_broker=message_broker,
    command_handlers=INJECTED_COMMAND_HANDLERS,
    query_handlers=INJECTED_QUERY_HANDLERS,
)

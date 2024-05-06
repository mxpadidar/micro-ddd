from auth.adapters.jwt_service_impl import JWTServiceImpl
from auth.adapters.orm.mapper import start_mappers
from auth.adapters.unit_of_work_impl import UnitOfWorkImpl
from auth.adapters.user_manager_impl import UserManagerImpl
from auth.service_layer.container import Container
from auth.service_layer.handlers import command_handlers_mapper
from shared.message_broker import MessageBroker, RedisMessageBroker
from shared.message_bus import MessageBus
from shared.settings import (
    ACCESS_TOKEN_LIFETIME,
    JWT_ALGORITHM,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT,
    SECRET_KEY,
    STORAGE_SERVICE_URL,
)
from shared.storage_service import StorageService
from shared.utils import inject_dependencies

start_mappers()


uow = UnitOfWorkImpl()

user_manager = UserManagerImpl(uow)

jwt_service = JWTServiceImpl(
    secret_key=SECRET_KEY,
    jwt_algorithm=JWT_ALGORITHM,
    access_token_lifetime=ACCESS_TOKEN_LIFETIME,
)

message_broker: MessageBroker = RedisMessageBroker(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB
)


storage_service = StorageService(STORAGE_SERVICE_URL)

container = Container(
    uow=uow,
    user_manager=user_manager,
    jwt_service=jwt_service,
    storage_service=storage_service,
    message_broker=message_broker,
)

DEPENDENCIES = {
    "uow": uow,
    "user_manager": user_manager,
    "jwt_service": jwt_service,
    "storage_service": storage_service,
    "message_broker": message_broker,
}


INJECTED_COMMAND_HANDLERS = {
    command_type: inject_dependencies(handler, DEPENDENCIES)
    for command_type, handler in command_handlers_mapper.items()
}


bus = MessageBus(
    uow=UnitOfWorkImpl(),
    message_broker=message_broker,
    command_handlers=INJECTED_COMMAND_HANDLERS,
)

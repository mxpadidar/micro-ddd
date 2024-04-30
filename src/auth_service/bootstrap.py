from auth_service.adapters.jwt_service_impl import JWTServiceImpl
from auth_service.adapters.orm.mapper import start_mappers
from auth_service.adapters.unit_of_work_impl import UnitOfWorkImpl
from auth_service.adapters.user_manager_impl import UserManagerImpl
from auth_service.service_layer.command_handlers import command_handlers_mapper
from auth_service.service_layer.query_handlers import query_handlers_mapper
from shared.broker_service import BrokerService, RabbitMQService
from shared.message_bus import MessageBus
from shared.settings import (
    ACCESS_TOKEN_LIFETIME,
    JWT_ALGORITHM,
    RABBITMQ_HOST,
    RABBITMQ_PASS,
    RABBITMQ_USER,
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


broker_service: BrokerService = RabbitMQService(
    host=RABBITMQ_HOST, user=RABBITMQ_USER, password=RABBITMQ_PASS
)

storage_service = StorageService(STORAGE_SERVICE_URL)

DEPENDENCIES = {
    "uow": uow,
    "user_manager": user_manager,
    "jwt_service": jwt_service,
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
    broker_service=broker_service,
    command_handlers=INJECTED_COMMAND_HANDLERS,
    query_handlers=INJECTED_QUERY_HANDLERS,
)

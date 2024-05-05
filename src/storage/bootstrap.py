from shared.auth_service import AuthService
from shared.message_broker import MessageBroker, RedisMessageBroker
from shared.message_bus import MessageBus
from shared.settings import (
    MINIO_ENDPOINT,
    MINIO_ROOT_PASSWORD,
    MINIO_ROOT_USER,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT,
)
from shared.utils import inject_dependencies
from storage.adapters.minio_client import MinioClient
from storage.adapters.orm.mapper import start_mappers
from storage.adapters.unit_of_work_impl import UnitOfWorkImpl
from storage.domain.s3_client import S3Client
from storage.service_layer.command_handlers import command_handlers_mapper
from storage.service_layer.container import Container
from storage.service_layer.query_handlers import query_handlers_mapper

start_mappers()


uow = UnitOfWorkImpl()

s3_client: S3Client = MinioClient(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
)

message_broker: MessageBroker = RedisMessageBroker(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB
)

auth_service = AuthService()

container = Container(
    uow=uow,
    s3_client=s3_client,
    message_broker=message_broker,
    auth_service=auth_service,
)


DEPENDENCIES = {"uow": uow, "s3_client": s3_client, "message_broker": message_broker}


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

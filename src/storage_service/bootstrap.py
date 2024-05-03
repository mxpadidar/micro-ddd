from shared.auth_service import AuthService
from shared.message_broker import MessageBroker, RedisMessageBroker
from shared.message_bus import MessageBus
from shared.settings import (
    MINIO_ACCESS_KEY,
    MINIO_ENDPOINT,
    MINIO_SECRET_KEY,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT,
)
from shared.utils import inject_dependencies
from storage_service.adapters.minio_client import MinioClient
from storage_service.adapters.orm.mapper import start_mappers
from storage_service.adapters.unit_of_work_impl import UnitOfWorkImpl
from storage_service.domain.s3_client import S3Client
from storage_service.service_layer.command_handlers import command_handlers_mapper
from storage_service.service_layer.query_handlers import query_handlers_mapper

start_mappers()


uow = UnitOfWorkImpl()

s3_client: S3Client = MinioClient(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
)

message_broker: MessageBroker = RedisMessageBroker(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB
)

auth_service = AuthService()


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

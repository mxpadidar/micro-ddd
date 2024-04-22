from shared.message_bus import MessageBus
from shared.settings import MINIO_ACCESS_KEY, MINIO_ENDPOINT, MINIO_SECRET_KEY
from shared.utils import inject_dependencies
from storage_service.adapters.minio_client import MinioClient
from storage_service.adapters.orm.mapper import start_mappers
from storage_service.adapters.unit_of_work_impl import UnitOfWorkImpl
from storage_service.service_layer.command_handlers import command_handlers_mapper

start_mappers()


uow = UnitOfWorkImpl()

s3_client = MinioClient(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    uow=uow,
)


DEPENDENCIES = {"uow": uow, "s3_client": s3_client}


INJECTED_COMMAND_HANDLERS = {
    command_type: inject_dependencies(handler, DEPENDENCIES)
    for command_type, handler in command_handlers_mapper.items()
}


bus = MessageBus(
    uow=UnitOfWorkImpl(),
    command_handlers=INJECTED_COMMAND_HANDLERS,
    query_handlers=dict(),
)
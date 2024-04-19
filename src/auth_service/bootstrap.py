from auth_service.adapters.auth_service_impl import AuthServiceImpl
from auth_service.adapters.orm.mapper import start_mappers
from auth_service.adapters.unit_of_work_impl import UnitOfWorkImpl
from auth_service.service_layer.command_handlers import command_handlers_mapper
from shared.message_bus import MessageBus
from shared.utils import inject_dependencies

start_mappers()


uow = UnitOfWorkImpl()

auth_service = AuthServiceImpl(uow=uow)

DEPENDENCIES = {"uow": uow, "auth_service": auth_service}


INJECTED_COMMAND_HANDLERS = {
    command_type: inject_dependencies(
        handler,
        DEPENDENCIES,
    )
    for command_type, handler in command_handlers_mapper.items()
}


bus = MessageBus(
    uow=UnitOfWorkImpl(),
    command_handlers=INJECTED_COMMAND_HANDLERS,
    query_handlers=dict(),
)

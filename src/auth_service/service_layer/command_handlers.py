from typing import Callable, Type

from auth_service.domain.unit_of_work import UnitOfWork
from auth_service.service_layer.commands import (
    UserAddAvatarCommand,
    UserAuthenticateCommand,
    UserRegisterCommand,
)
from shared.auth_service import AuthService
from shared.base import BaseCommand
from shared.errors import InvalidCredentialsError
from shared.storage_service import StorageService


def user_register_handler(command: UserRegisterCommand, auth_service: AuthService):
    user = auth_service.register_user(command.email, command.password)
    return user


def user_authenticate_handler(
    command: UserAuthenticateCommand, auth_service: AuthService
):
    user = auth_service.authenticate_user(command.email, command.password)
    if not user:
        raise InvalidCredentialsError
    token = auth_service.generate_token(user)
    return token


async def user_add_avatar_handler(
    command: UserAddAvatarCommand, uow: UnitOfWork, storage_service: StorageService
):
    with uow:
        user = uow.users.get(id=command.user_id)
        avatar_url = await storage_service.get_file_by_id(command.file_id)
        user.avatar_file_id = command.file_id
        uow.users.add(user)
        uow.commit()
        return user.serialize(avatar=avatar_url)


command_handlers_mapper: dict[Type[BaseCommand], Callable] = {
    UserRegisterCommand: user_register_handler,
    UserAuthenticateCommand: user_authenticate_handler,
    UserAddAvatarCommand: user_add_avatar_handler,
}

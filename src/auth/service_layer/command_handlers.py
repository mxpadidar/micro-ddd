from datetime import datetime
from typing import Callable, Type
from xml.dom import NotFoundErr

from auth.domain.jwt_service import JWTService
from auth.domain.unit_of_work import UnitOfWork
from auth.domain.user_manager import UserManager
from auth.service_layer.commands import (
    UserAddAvatarCommand,
    UserAuthenticateCommand,
    UserRegisterCommand,
    VerifyTokenCommand,
)
from shared.base import Command
from shared.dtos import TokenPayload
from shared.errors import ConflictError, InvalidCredentialsError
from shared.storage_service import StorageService


def verify_token_handler(
    command: VerifyTokenCommand, user_manager: UserManager, jwt_service: JWTService
):
    try:
        payload = jwt_service.decode(command.token)
        return user_manager.get_user_by_email(payload.email).serialize()
    except InvalidCredentialsError:
        raise InvalidCredentialsError
    except NotFoundErr:
        raise InvalidCredentialsError


def user_register_handler(command: UserRegisterCommand, user_manager: UserManager):
    try:
        user = user_manager.create_user(command.email, command.password)
        return user
    except ConflictError:
        raise ConflictError


def user_authenticate_handler(
    command: UserAuthenticateCommand, user_manager: UserManager, jwt_service: JWTService
):
    try:
        user = user_manager.authenticate_user(command.email, command.password)
        return jwt_service.encode(
            TokenPayload(
                email=user.email,
                expires_at=datetime.now() + jwt_service.access_token_lifetime,
            )
        )
    except InvalidCredentialsError:
        raise InvalidCredentialsError


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


command_handlers_mapper: dict[Type[Command], Callable] = {
    UserRegisterCommand: user_register_handler,
    UserAuthenticateCommand: user_authenticate_handler,
    UserAddAvatarCommand: user_add_avatar_handler,
    VerifyTokenCommand: verify_token_handler,
}

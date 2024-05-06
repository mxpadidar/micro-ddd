from datetime import datetime
from typing import Callable, Type
from xml.dom import NotFoundErr

from auth.domain.jwt_service import JWTService
from auth.domain.user_manager import UserManager
from auth.service_layer import messages
from shared.base import Command
from shared.dtos import TokenPayload
from shared.errors import ConflictError, InvalidCredentialsError
from shared.message_broker import MessageBroker
from shared.storage_service import StorageService


def verify_token_handler(
    command: messages.VerifyTokenCommand,
    user_manager: UserManager,
    jwt_service: JWTService,
):
    try:
        payload = jwt_service.decode(command.token)
        return user_manager.get_user_by_email(payload.email).serialize()
    except InvalidCredentialsError:
        raise InvalidCredentialsError
    except NotFoundErr:
        raise InvalidCredentialsError


async def user_register_handler(
    command: messages.UserRegisterCommand,
    user_manager: UserManager,
    storage_service: StorageService,
    message_broker: MessageBroker,
):
    try:
        user = user_manager.create_user(command.email, command.password)
        if not command.avatar_file_id:
            return user
        avatar_file = await storage_service.get_file_by_id(command.avatar_file_id)
        user.avatar_file_id = avatar_file.id
        event = messages.FileUsedEvent(file_id=avatar_file.id, user_id=user.id)
        message_broker.publish(destination="file_used", message=event.to_dict())
        return user
    except ConflictError:
        raise ConflictError


def user_authenticate_handler(
    command: messages.UserAuthenticateCommand,
    user_manager: UserManager,
    jwt_service: JWTService,
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


command_handlers_mapper: dict[Type[Command], Callable] = {
    messages.UserRegisterCommand: user_register_handler,
    messages.UserAuthenticateCommand: user_authenticate_handler,
    messages.VerifyTokenCommand: verify_token_handler,
}

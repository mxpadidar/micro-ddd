from typing import Callable, Type

from auth_service.service_layer.commands import (
    UserAuthenticateCommand,
    UserRegisterCommand,
)
from shared.auth_service import AuthService
from shared.base import BaseCommand
from shared.exceptions import InvalidCredentialsException


def user_register_handler(command: UserRegisterCommand, auth_service: AuthService):
    user = auth_service.register_user(command.email, command.password)
    return user


def user_authenticate_handler(
    command: UserAuthenticateCommand, auth_service: AuthService
):
    user = auth_service.authenticate_user(command.email, command.password)
    if not user:
        raise InvalidCredentialsException
    token = auth_service.generate_token(user)
    return token


command_handlers_mapper: dict[Type[BaseCommand], Callable] = {
    UserRegisterCommand: user_register_handler,
    UserAuthenticateCommand: user_authenticate_handler,
}

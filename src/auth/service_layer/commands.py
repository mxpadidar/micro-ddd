from dataclasses import dataclass

from shared.base import Command


@dataclass
class UserRegisterCommand(Command):
    email: str
    password: str


@dataclass
class UserAuthenticateCommand(Command):
    email: str
    password: str


@dataclass
class UserAddAvatarCommand(Command):
    user_id: int
    file_id: int


@dataclass
class VerifyTokenCommand(Command):
    token: str

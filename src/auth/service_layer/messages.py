from dataclasses import dataclass

from shared.base import Command, Event


@dataclass
class UserRegisterCommand(Command):
    email: str
    password: str
    avatar_file_id: int | None


@dataclass
class UserAuthenticateCommand(Command):
    email: str
    password: str


@dataclass
class VerifyTokenCommand(Command):
    token: str


@dataclass
class FileUsedEvent(Event):
    file_id: int
    user_id: int

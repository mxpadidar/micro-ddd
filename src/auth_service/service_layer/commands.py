from dataclasses import dataclass

from shared.base import BaseCommand


@dataclass
class UserRegisterCommand(BaseCommand):
    email: str
    password: str


@dataclass
class UserAuthenticateCommand(BaseCommand):
    email: str
    password: str


@dataclass
class UserAddAvatarCommand(BaseCommand):
    user_id: int
    file_id: int


@dataclass
class VerifyTokenCommand(BaseCommand):
    token: str

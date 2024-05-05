from dataclasses import dataclass

from shared.base import Command
from shared.dtos import UserDto


@dataclass
class CreateProduct(Command):
    user: UserDto
    name: str
    price: float
    avatar_file_id: int

from dataclasses import dataclass

from shared.base import Command
from shared.protocols import UserProtocol


@dataclass
class CreateProduct(Command):
    user: UserProtocol
    name: str
    price: float

from dataclasses import dataclass

from shared.base import BaseCommand


@dataclass
class CreateFileCommand(BaseCommand):
    file_bytes: bytes
    category: str
    name: str

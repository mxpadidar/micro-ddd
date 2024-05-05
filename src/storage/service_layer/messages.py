from dataclasses import dataclass

from shared.base import Command, Event, Query
from shared.dtos import UserDto
from storage.domain.enums import FileBucket


@dataclass
class GetFileQuery(Query):
    file_id: int


@dataclass
class CreateFileCommand(Command):
    file_bytes: bytes
    bucket: FileBucket
    name: str | None
    user: UserDto


@dataclass
class FileCreatedEvent(Event):
    file_id: int
    user: UserDto

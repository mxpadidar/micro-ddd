from dataclasses import dataclass

from shared.base import Command, Event, Query
from shared.protocols import UserProtocol


@dataclass
class GetFileQuery(Query):
    file_id: int


@dataclass
class CreateFileCommand(Command):
    file_bytes: bytes
    category: str
    name: str
    user: UserProtocol

    def to_dict(self) -> dict:
        return {"category": self.category, "name": self.name, "user": self.user}


@dataclass
class FileCreatedEvent(Event):
    file_id: int
    user: UserProtocol

    def to_dict(self) -> dict:
        return {"file_id": self.file_id, "user": self.user}

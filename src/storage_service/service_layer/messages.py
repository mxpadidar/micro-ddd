from dataclasses import dataclass

from shared.base import BaseCommand, BaseEvent, BaseQuery
from shared.protocols import UserProtocol


@dataclass
class GetFileQuery(BaseQuery):
    file_id: int


@dataclass
class CreateFileCommand(BaseCommand):
    file_bytes: bytes
    category: str
    name: str
    user: UserProtocol

    def to_dict(self) -> dict:
        return {"category": self.category, "name": self.name, "user": self.user}


@dataclass
class FileCreatedEvent(BaseEvent):
    file_id: int
    user: UserProtocol

    def to_dict(self) -> dict:
        return {"file_id": self.file_id, "user": self.user}

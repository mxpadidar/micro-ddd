from abc import ABC
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum


class BaseModel(ABC):
    id: int

    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def serialize(self, **kwargs) -> dict:
        return self.__dict__


class BaseUnitOfWork(ABC): ...


class BaseCommand: ...


class BaseEvent: ...


class BaseQuery: ...


class BaseEnum(Enum): ...


class BaseError(Exception): ...


@dataclass
class BaseDto:

    def to_dict(self) -> dict:
        return asdict(self)

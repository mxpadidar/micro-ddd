from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class BaseModel(ABC):
    id: int

    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None
    events: list = list()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def serialize(self, **kwargs) -> dict:
        return self.__dict__


class BaseRepo(ABC):

    seen: set = set()

    def add(self, entity: BaseModel) -> None:
        self._add(entity)
        self.seen.add(entity)

    def get(self, id: int) -> Any:
        entity = self._get(id)
        self.seen.add(entity)
        return entity

    @abstractmethod
    def _get(self, id: int) -> BaseModel: ...

    @abstractmethod
    def _add(self, entity: BaseModel) -> None: ...


class BaseUnitOfWork(ABC):

    repositories: set[BaseRepo] = set()

    def commit(self) -> None:
        self._commit()

    @abstractmethod
    def _commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...

    def collect_new_events(self):
        for repo in self.repositories:
            for entity in repo.seen:
                while entity.events:
                    yield entity.events.pop(0)


@dataclass
class BaseCommand:
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BaseEvent:

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BaseQuery:

    def to_dict(self) -> dict:
        return asdict(self)


class BaseEnum(Enum): ...


class BaseError(Exception): ...


@dataclass
class BaseDto:

    def to_dict(self) -> dict:
        return asdict(self)

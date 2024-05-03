from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class BaseEntity(ABC):
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

    def add(self, entity: BaseEntity) -> None:
        self._add(entity)
        self.seen.add(entity)

    def get(self, id: int) -> Any:
        entity = self._get(id)
        self.seen.add(entity)
        return entity

    @abstractmethod
    def _get(self, id: int) -> BaseEntity: ...

    @abstractmethod
    def _add(self, entity: BaseEntity) -> None: ...


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
class BaseMessage(ABC):

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Command(BaseMessage): ...


@dataclass
class Event(BaseMessage): ...


@dataclass
class Query(BaseMessage): ...


class BaseEnum(Enum): ...


class BaseError(Exception): ...


@dataclass
class BaseDto:

    def to_dict(self) -> dict:
        return asdict(self)

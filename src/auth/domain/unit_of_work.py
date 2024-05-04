from abc import ABC, abstractmethod

from auth.domain.repositories.user_repo import UserRepo
from shared.base import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork, ABC):
    users: UserRepo

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abstractmethod
    def _commit(self): ...

    @abstractmethod
    def rollback(self): ...

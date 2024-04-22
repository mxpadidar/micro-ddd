from abc import ABC, abstractmethod

from shared.base import BaseUnitOfWork
from storage_service.domain.repositories.file_repo import FileRepo


class UnitOfWork(BaseUnitOfWork, ABC):
    files: FileRepo

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.rollback()

    def commit(self) -> None:
        self._commit()

    @abstractmethod
    def _commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...

from shared.base import BaseUnitOfWork
from storage.domain.repositories.file_repo import FileRepo


class UnitOfWork(BaseUnitOfWork):
    files: FileRepo

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.rollback()

from sqlalchemy.orm import Session

from shared.db_setup import sessionmaker
from storage_service.adapters.repositories.file_repo_impl import FileRepoImpl
from storage_service.domain.unit_of_work import UnitOfWork


class UnitOfWorkImpl(UnitOfWork):

    def __init__(self, sessionmaker=sessionmaker) -> None:
        self.sessionmaker = sessionmaker

    def __enter__(self) -> UnitOfWork:
        self.session: Session = self.sessionmaker()
        self.files = FileRepoImpl(self.session)
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def _commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

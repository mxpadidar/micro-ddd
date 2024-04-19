from auth_service.adapters.repositories.user_repo_impl import UserRepoImpl
from auth_service.domain.unit_of_work import UnitOfWork
from shared.db_setup import sessionmaker


class UnitOfWorkImpl(UnitOfWork):

    def __init__(self, sessionmaker=sessionmaker):
        self.sessionmaker = sessionmaker

    def __enter__(self):
        self.session = self.sessionmaker()
        self.users = UserRepoImpl(self.session)
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

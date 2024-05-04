from product.adapters.repositories.product_repo_impl import ProductRepoImpl
from product.domain.unit_of_work import UnitOfWork
from shared.db_setup import sessionmaker


class UnitOfWorkImpl(UnitOfWork):

    def __init__(self, sessionmaker=sessionmaker):
        self.sessionmaker = sessionmaker
        self.repos = set()

    def __enter__(self):
        self.session = self.sessionmaker()
        self.products = ProductRepoImpl(self.session)
        self.repos.add(self.products)
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

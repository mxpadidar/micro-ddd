from abc import ABC, abstractmethod

from product.domain.repositories.product_repo import ProductRepo
from shared.base import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork, ABC):
    products: ProductRepo

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

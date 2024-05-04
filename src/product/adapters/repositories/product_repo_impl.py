from sqlalchemy.orm import Session

from product.domain.entities.product import Product
from product.domain.repositories.product_repo import ProductRepo
from shared.errors import NotFoundError


class ProductRepoImpl(ProductRepo):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _add(self, product: Product) -> None:
        self.session.add(product)

    def _get(self, id: int) -> Product:
        product = self.session.query(Product).filter_by(id=id).first()
        if not product:
            raise NotFoundError
        return product

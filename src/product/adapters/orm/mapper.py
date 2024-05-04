from product.adapters.orm.tables import products
from product.domain.entities.product import Product
from shared.db_setup import registry


def start_mappers():
    registry.map_imperatively(Product, products)

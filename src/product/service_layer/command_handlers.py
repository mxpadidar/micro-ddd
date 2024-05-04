from typing import Callable, Type

from product.domain.entities.product import Product
from product.domain.unit_of_work import UnitOfWork
from product.service_layer import messages
from shared.base import Command


def create_product_handler(command: messages.CreateProduct, uow: UnitOfWork):
    with uow:
        product = Product(name=command.name, price=command.price)
        uow.products.add(product)
        uow.commit()
        return product.serialize()


command_handlers_mapper: dict[Type[Command], Callable] = {
    messages.CreateProduct: create_product_handler
}

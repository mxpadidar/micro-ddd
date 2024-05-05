from typing import Callable, Type

from product.domain.entities.product import Product
from product.domain.unit_of_work import UnitOfWork
from product.service_layer import messages
from shared.base import Command
from shared.storage_service import StorageService


async def create_product_handler(
    command: messages.CreateProduct, uow: UnitOfWork, storage_service: StorageService
):
    with uow:
        file = await storage_service.get_file_by_id(command.avatar_file_id)

        product = Product(
            name=command.name, price=command.price, avatar_file_id=file.id
        )
        uow.products.add(product)
        uow.commit()
        # TODO publish event to update file.used
        return product.serialize()


command_handlers_mapper: dict[Type[Command], Callable] = {
    messages.CreateProduct: create_product_handler
}

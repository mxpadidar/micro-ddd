from fastapi import APIRouter, Depends

from product.bootstrap import bus
from product.entrypoints import request_models as rm
from product.entrypoints.dependencies import current_user
from product.service_layer.messages import CreateProduct
from shared.protocols import UserProtocol

router = APIRouter(prefix="/product", tags=["Product"])


@router.post("")
def create_product(
    data: rm.CreateProductRequest, user: UserProtocol = Depends(current_user)
):
    command = CreateProduct(user=user, name=data.name, price=data.price)
    return bus.handle(command)

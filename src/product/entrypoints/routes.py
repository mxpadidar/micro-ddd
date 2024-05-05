from fastapi import APIRouter, Depends

from product.bootstrap import bus
from product.entrypoints import request_models as rm
from product.entrypoints.dependencies import current_user
from product.service_layer.messages import CreateProduct
from shared.dtos import UserDto

router = APIRouter(prefix="/product", tags=["Product"])


@router.post("")
async def create_product(
    data: rm.CreateProductRequest, user: UserDto = Depends(current_user)
):
    command = CreateProduct(
        user=user,
        name=data.name,
        price=data.price,
        avatar_file_id=data.avatar_file_id,
    )
    return await bus.handle(command)

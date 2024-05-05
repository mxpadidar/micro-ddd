from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    name: str
    price: float
    avatar_file_id: int

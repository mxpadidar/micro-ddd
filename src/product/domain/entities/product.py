from shared.base import BaseEntity


class Product(BaseEntity):
    name: str
    price: float
    avatar_file_id: int

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def add_avatar(self, file_id: int) -> None:
        self.avatar_file_id = file_id

    def serialize(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "avatar": kwargs.pop("avatar", self.avatar_file_id),
            **kwargs,
        }

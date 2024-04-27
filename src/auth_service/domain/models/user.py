from shared.base import BaseModel


class User(BaseModel):
    email: str
    hashed_password: str
    is_superuser: bool
    is_active: bool
    avatar_file_id: int | None

    def __init__(
        self, email: str, hashed_password: str, is_superuser: bool = False
    ) -> None:
        self.email = email
        self.hashed_password = hashed_password
        self.is_superuser = is_superuser
        self.is_active = True

    def add_avatar(self, file_id: int) -> None:
        self.avatar_file_id = file_id

    def serialize(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "is_superuser": self.is_superuser,
            "is_active": self.is_active,
            "avatar": kwargs.pop("avatar", self.avatar_file_id),
            **kwargs,
        }

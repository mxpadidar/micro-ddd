from shared.base import BaseModel


class User(BaseModel):
    email: str
    hashed_password: str
    is_superuser: bool
    is_active: bool

    def __init__(
        self, email: str, hashed_password: str, is_superuser: bool = False
    ) -> None:
        self.email = email
        self.hashed_password = hashed_password
        self.is_superuser = is_superuser
        self.is_active = True

    def serialize(self, **kwargs) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "is_superuser": self.is_superuser,
            "is_active": self.is_active,
            **kwargs,
        }

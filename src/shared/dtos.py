from dataclasses import dataclass
from datetime import datetime

from shared.base import BaseDto


@dataclass
class TokenPayload(BaseDto):
    email: str
    expires_at: datetime

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "expires_at": self.expires_at.isoformat(),
        }


@dataclass
class TokenDto(BaseDto):
    access_token: str


@dataclass
class UserDto(BaseDto):
    id: int
    email: str
    is_active: bool
    avatar: int | None

    @classmethod
    def from_dict(cls, data: dict) -> "UserDto":
        return cls(
            id=data["id"],
            email=data["email"],
            is_active=data["is_active"],
            avatar=data.get("avatar"),
        )


@dataclass
class FileDto(BaseDto):
    id: int
    name: str
    url: str

    @classmethod
    def from_dict(cls, data: dict) -> "FileDto":
        return cls(
            id=data["id"],
            name=data["name"],
            url=data["url"],
        )

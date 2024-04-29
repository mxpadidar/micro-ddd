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
class FileDto(BaseDto):
    id: int
    object_name: str
    url: str

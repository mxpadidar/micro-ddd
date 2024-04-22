from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenPayload:
    user_id: int
    expires_at: datetime


@dataclass
class FileDTO:
    id: int
    object_name: str
    url: str

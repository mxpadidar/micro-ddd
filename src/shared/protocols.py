from typing import Protocol


class UserProtocol(Protocol):
    id: int
    email: str

    def serialize(self, **kwargs) -> dict: ...

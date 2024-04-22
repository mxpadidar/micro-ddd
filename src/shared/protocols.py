from typing import Protocol


class UserProtocol(Protocol):
    id: int
    email: str

    def serialize(self, **kwargs) -> dict: ...


class FileProtocol(Protocol):
    id: int
    object_name: str
    url: str

    def serialize(self, **kwargs) -> dict: ...

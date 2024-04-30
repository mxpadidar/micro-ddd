from abc import ABC, abstractmethod


class S3Client(ABC):

    @abstractmethod
    def upload(self, file: bytes, object_name) -> None: ...

    @abstractmethod
    def delete(self, object_name: str) -> None: ...

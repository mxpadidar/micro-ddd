from abc import ABC, abstractmethod


class S3Client(ABC):

    @abstractmethod
    def upload(self, file: bytes, bucket: str, file_name: str) -> None: ...

    @abstractmethod
    def delete(self, bucket: str, file_name: str) -> None: ...

    @abstractmethod
    def get_file_url(self, bucket: str, file_name: str) -> str: ...

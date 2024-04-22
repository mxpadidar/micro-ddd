from abc import ABC, abstractmethod

from storage_service.domain.models.file import File


class FileRepo(ABC):

    @abstractmethod
    def add(self, file: File) -> None: ...

    @abstractmethod
    def get(self, id: int) -> File: ...

    @abstractmethod
    def refresh(self, file: File) -> None: ...

from abc import ABC, abstractmethod

from shared.base import BaseRepo
from storage_service.domain.models.file import File


class FileRepo(BaseRepo, ABC):

    @abstractmethod
    def refresh(self, file: File) -> None: ...

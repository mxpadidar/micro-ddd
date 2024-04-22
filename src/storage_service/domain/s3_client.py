import os
from abc import ABC, abstractmethod
from uuid import uuid4

from magic import Magic

from shared.errors import InvalidRequestError
from shared.logger import Logger
from storage_service.domain.errors import FileDeleteError, FileUploadError
from storage_service.domain.models.file import File
from storage_service.domain.unit_of_work import UnitOfWork

logger = Logger("S3 Client")


class S3Client(ABC):
    valid_mime_types: list[str] = ["image/jpeg", "image/png"]

    def __init__(self, uow: UnitOfWork) -> None:

        self.uow = uow

    def get_file_by_id(self, file_id: int) -> str:
        """Return the file url by file id."""

        with self.uow:
            file = self.uow.files.get(id=file_id)
            return f"{self.base_url}/{file.object_name}"

    def upload_file(self, file_bytes: bytes, category: str, name: str) -> File:

        file_name = self._generate_unique_filename(name)
        file_size = len(file_bytes)
        file_mime_type = self._get_mime_type(file_bytes)
        with self.uow:
            try:
                self._upload(file_bytes, category, file_name, file_size)
                file = File(
                    category=category,
                    name=file_name,
                    mime_type=file_mime_type,
                    size=file_size,
                )
                self.uow.files.add(file)
                return file
            except Exception as error:
                logger.exception(f"Error uploading file: {error}")
                raise FileUploadError

    def delete(self, object_name: str) -> None:
        try:
            self._delete(object_name)
        except Exception as error:
            logger.exception(f"Error deleting file: {error}")
            raise FileDeleteError

    def _generate_unique_filename(self, name: str) -> str:
        """Generate a unique filename."""

        _, extension = os.path.splitext(name)

        if not extension:
            raise InvalidRequestError("Invalid file extension")

        return str(uuid4()) + extension

    def _get_mime_type(self, file_content: bytes) -> str:
        """
        Determine the MIME type of the given file content. If the MIME type is not valid, an exception is raised.
        """
        mime = Magic(mime=True)
        mime_type = mime.from_buffer(file_content)
        if mime_type not in self.valid_mime_types:
            raise InvalidRequestError("Invalid file type")
        return mime_type

    @abstractmethod
    def _upload(self, file_bytes: bytes, category: str, name: str, size: int) -> str:
        """Upload a file to the S3 and return the object name"""

    @abstractmethod
    def _delete(self, object_name: str) -> None:
        """Delete a file from the S3"""

    @property
    @abstractmethod
    def base_url(self) -> str:
        """Return the base url"""

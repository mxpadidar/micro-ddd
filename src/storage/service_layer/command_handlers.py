import os
from typing import Callable, Type
from uuid import uuid4

from magic import Magic

from shared.base import Command
from shared.errors import InvalidRequestError
from storage.domain.entities.file import File
from storage.domain.s3_client import S3Client
from storage.domain.unit_of_work import UnitOfWork
from storage.service_layer.messages import CreateFileCommand, FileCreatedEvent


def create_file_handler(
    command: CreateFileCommand, uow: UnitOfWork, s3_client: S3Client
) -> dict:

    if not command.name:
        raise InvalidRequestError

    mime_type = get_mime_type(command.file_bytes)

    if mime_type not in File.valid_mime_types():
        raise InvalidRequestError("Invalid file type")

    name = generate_unique_filename(command.name)
    size = len(command.file_bytes)

    s3_client.upload(
        file=command.file_bytes, bucket=command.bucket.value, file_name=command.name
    )

    file = File(bucket=command.bucket.value, name=name, mime_type=mime_type, size=size)

    with uow:
        uow.files.add(file)
        uow.commit()
        file.events.append(FileCreatedEvent(file_id=file.id, user=command.user))

    return file.serialize()


command_handlers_mapper: dict[Type[Command], Callable] = {
    CreateFileCommand: create_file_handler,
}


def generate_unique_filename(name: str) -> str:
    """Generate a unique filename."""

    _, extension = os.path.splitext(name)

    if not extension:
        raise ValueError("Invalid file extension")

    return str(uuid4()) + extension


def get_mime_type(file_content: bytes) -> str:
    """
    Determine the MIME type of the given file content.
    """
    mime = Magic(mime=True)
    mime_type = mime.from_buffer(file_content)
    return mime_type

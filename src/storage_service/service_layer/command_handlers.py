from typing import Callable, Type

from shared.base import BaseCommand
from storage_service.domain.s3_client import S3Client
from storage_service.service_layer.commands import CreateFileCommand


def create_file_handler(command: CreateFileCommand, s3_client: S3Client) -> dict:

    file = s3_client.upload_file(
        file_bytes=command.file_bytes,
        category=command.category,
        name=command.name,
    )
    return file.serialize()


command_handlers_mapper: dict[Type[BaseCommand], Callable] = {
    CreateFileCommand: create_file_handler,
}

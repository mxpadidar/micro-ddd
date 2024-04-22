from typing import Callable, Type

from shared.base import BaseQuery
from storage_service.domain.s3_client import S3Client
from storage_service.service_layer.queries import GetFileQuery


def get_file_url(query: GetFileQuery, s3_client: S3Client) -> str:
    return s3_client.get_file_by_id(query.file_id)


query_handlers: dict[Type[BaseQuery], Callable] = {
    GetFileQuery: get_file_url,
}
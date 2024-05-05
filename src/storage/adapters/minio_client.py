from io import BytesIO

from minio import Minio

from shared.logger import Logger
from storage.domain.errors import FileDeleteError, FileUploadError
from storage.domain.s3_client import S3Client

logger = Logger("Minio client")


class MinioClient(S3Client):

    _client: Minio | None = None

    def __init__(self, endpoint: str, access_key: str, secret_key: str) -> None:
        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key

    @property
    def client(self) -> Minio:
        if self._client is None:

            self._client = Minio(
                endpoint=self._endpoint,
                access_key=self._access_key,
                secret_key=self._secret_key,
                secure=False,
            )
        return self._client

    def upload(self, file: bytes, bucket: str, file_name: str) -> None:
        self._ensure_bucket_exists(bucket)
        try:
            self.client.put_object(
                data=BytesIO(file),
                bucket_name=bucket,
                object_name=file_name,
                length=len(file),
            )
        except Exception as error:
            logger.error(f"Error uploading file: {error}")
            raise FileUploadError

    def delete(self, bucket: str, file_name: str) -> None:
        try:
            self.client.remove_object(bucket_name=bucket, object_name=file_name)
        except Exception as error:
            logger.error(f"Error deleting file: {error}")
            raise FileDeleteError

    def get_file_url(self, bucket: str, file_name: str) -> str:
        return self.client.presigned_get_object(
            bucket_name=bucket, object_name=file_name
        )

    def _ensure_bucket_exists(self, bucket: str):
        if not self.client.bucket_exists(bucket_name=bucket):
            self.client.make_bucket(bucket)

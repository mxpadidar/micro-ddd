from io import BytesIO

from minio import Minio

from storage_service.domain.s3_client import S3Client
from storage_service.domain.unit_of_work import UnitOfWork


class MinioClient(S3Client):

    _client: Minio | None = None

    def __init__(
        self,
        uow: UnitOfWork,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str = "default",
    ) -> None:
        self._endpoint = endpoint
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket = bucket
        super().__init__(uow)

    @property
    def base_url(self) -> str:
        return f"{self._endpoint}/{self._bucket}"

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

    def _upload(self, file: bytes, category: str, name: str, size: int) -> str:
        res = self.client.put_object(
            data=BytesIO(file),
            bucket_name=self._bucket,
            object_name=f"{category}/{name}",
            length=size,
        )
        return res.object_name

    def _delete(self, object_name: str) -> None:
        self.client.remove_object(bucket_name=self._bucket, object_name=object_name)

from storage.domain.s3_client import S3Client
from storage.domain.unit_of_work import UnitOfWork
from storage.entrypoints.response_models import FileResponse


def file_details_view(
    file_id: int, uow: UnitOfWork, s3_client: S3Client
) -> FileResponse:
    with uow:
        file = uow.files.get(file_id)
        url = s3_client.get_file_url(file.bucket, file.name)
        return FileResponse(id=file.id, name=file.name, url=url)

from fastapi import APIRouter, Depends, File, Form, UploadFile

from shared.dtos import UserDto
from storage.bootstrap import bus, container
from storage.domain.enums import FileBucket
from storage.entrypoints import views
from storage.entrypoints.dependencies import current_user
from storage.service_layer.messages import CreateFileCommand

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    bucket: FileBucket = Form(...),
    user: UserDto = Depends(current_user),
):
    command = CreateFileCommand(
        file_bytes=await file.read(),
        bucket=bucket,
        name=file.filename,
        user=user,
    )
    return bus.handle(command)


@router.get("/{file_id}")
async def file_details_view(file_id: int):
    return views.file_details_view(file_id, container.uow, container.s3_client)

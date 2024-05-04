from fastapi import APIRouter, Depends, File, Form, UploadFile

from shared.protocols import UserProtocol
from storage.bootstrap import bus
from storage.entrypoints.dependencies import current_user
from storage.service_layer.messages import CreateFileCommand, GetFileQuery

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    category: str = Form(...),
    user: UserProtocol = Depends(current_user),
):
    command = CreateFileCommand(
        file_bytes=await file.read(),
        category=category,
        name=file.filename or "some_file_name",
        user=user,
    )
    return bus.handle(command)


@router.get("/{file_id}")
async def get_file_url(file_id: int):
    query = GetFileQuery(file_id=file_id)
    return bus.handle(query)

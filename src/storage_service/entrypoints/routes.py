from fastapi import APIRouter, File, Form, UploadFile

from storage_service.bootstrap import bus
from storage_service.service_layer.commands import CreateFileCommand
from storage_service.service_layer.queries import GetFileQuery

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.post("")
async def upload_file(file: UploadFile = File(...), category: str = Form(...)):
    command = CreateFileCommand(
        file_bytes=await file.read(),
        category=category,
        name=file.filename or "some_file_name",
    )
    return bus.handle(command)


@router.get("/{file_id}")
async def get_file_url(file_id: int):
    query = GetFileQuery(file_id=file_id)
    return bus.handle(query)

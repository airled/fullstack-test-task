import uuid

from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db import get_db
from src.types import Err
from fastapi import APIRouter, HTTPException
from src.files.schemas import FileItem, FileUpdate
from src.files.services.list_files import list_files
from src.files.services.create_file import create_file
from src.files.services.get_file import get_file
from src.files.services.update_file import update_file
from src.files.services.get_file_and_path import get_file_and_path
from src.files.services.delete_file import delete_file
from fastapi import File, Form, UploadFile, Depends
from fastapi.responses import FileResponse
from starlette import status

router = APIRouter()

@router.get("/files", response_model=list[FileItem])
async def list_files_view(
    offset: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_db),
):
    list_files_result = await list_files(session=session, offset=offset, limit=limit)
    if isinstance(list_files_result, Err):
        return []

    return list_files_result.value

@router.post("/files", response_model=FileItem, status_code=201)
async def create_file_view(
    title: str = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
):
    file_item_result = await create_file(session=session, title=title, upload_file=file)
    if isinstance(file_item_result, Err):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=file_item_result.error,
        )

    return file_item_result.value

@router.get("/files/{file_id}", response_model=FileItem)
async def get_file_view(
    file_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    get_file_result = await get_file(session=session, file_id=file_id)
    if isinstance(get_file_result, Err):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=get_file_result.error,
        )

    return get_file_result.value

@router.patch("/files/{file_id}", response_model=FileItem)
async def update_file_view(
    file_id: uuid.UUID,
    payload: FileUpdate,
    session: AsyncSession = Depends(get_db),
):
    update_file_result = await update_file(session=session, file_id=file_id, title=payload.title)
    if isinstance(update_file_result, Err):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=update_file_result.error)

    return update_file_result.value

@router.get("/files/{file_id}/download")
async def download_file(
    file_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    get_file_and_path_result = await get_file_and_path(session=session, file_id=file_id)
    if isinstance(get_file_and_path_result, Err):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=get_file_and_path_result.error,
        )

    file_item, stored_path = get_file_and_path_result.value
    return FileResponse(
        path=stored_path,
        media_type=file_item.mime_type,
        filename=file_item.original_name,
    )

@router.delete("/files/{file_id}", status_code=204)
async def delete_file_view(
    file_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    delete_file_result = await delete_file(session=session, file_id=file_id)
    if isinstance(delete_file_result, Err):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=delete_file_result.error,
        )

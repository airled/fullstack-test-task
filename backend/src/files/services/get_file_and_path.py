import uuid

from sqlalchemy.ext.asyncio.session import AsyncSession
from src.types import Result, Ok, Err
from src.files.model import StoredFile
from pathlib import Path
from .get_file import get_file
from src.storage_dir import STORAGE_DIR

async def get_file_and_path(session: AsyncSession, file_id: uuid.UUID) -> Result[tuple[StoredFile, Path]]:
    file_item_result = await get_file(session, file_id)
    if isinstance(file_item_result, Err):
        return file_item_result

    file_item = file_item_result.value
    stored_path = STORAGE_DIR / file_item.stored_name
    if not stored_path.exists():
        return Err('Stored file not found')

    return Ok((file_item, stored_path))

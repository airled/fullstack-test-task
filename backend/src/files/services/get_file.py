import uuid

from sqlalchemy.ext.asyncio.session import AsyncSession
from src.types import Result, Ok, Err
from src.files.model import StoredFile

async def get_file(session: AsyncSession, file_id: uuid.UUID) -> Result[StoredFile]:
    file_item = await session.get(StoredFile, file_id)
    if not file_item:
        return Err('File not found')

    return Ok(file_item)

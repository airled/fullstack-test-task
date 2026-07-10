from src.types import Result, Ok
from src.files.model import StoredFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

async def list_files(session: AsyncSession, offset: int, limit: int) -> Result[list[StoredFile]]:
    result = await session.execute(
        select(StoredFile).order_by(StoredFile.created_at.desc()).offset(offset).limit(limit)
    )
    return Ok(list(result.scalars().all()))

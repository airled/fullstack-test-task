import uuid

from sqlalchemy.ext.asyncio.session import AsyncSession
from src.types import Result, Ok, Err
from .get_file_and_path import get_file_and_path

async def delete_file(session: AsyncSession, file_id: uuid.UUID) -> Result[str]:
    get_file_and_path_result = await get_file_and_path(session, file_id)
    if isinstance(get_file_and_path_result, Err):
        return get_file_and_path_result

    file_item, stored_path = get_file_and_path_result.value
    if stored_path.exists():
        stored_path.unlink()
    await session.delete(file_item)
    await session.commit()
    return Ok('ok')

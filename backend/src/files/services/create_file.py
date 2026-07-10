import mimetypes
from fastapi import UploadFile
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.types import Result, Ok, Err
from src.files.model import ProcessingStatus, StoredFile
from pathlib import Path
from uuid import uuid4
from src.tasks import process_scan_file_for_threats
from src.storage_dir import STORAGE_DIR

async def create_file(session: AsyncSession, title: str, upload_file: UploadFile) -> Result[StoredFile]:
    content = await upload_file.read()
    if not content:
        return Err('File is empty')

    file_id = uuid4()
    suffix = Path(upload_file.filename or "").suffix
    stored_name = f"{str(file_id)}{suffix}"
    stored_path = STORAGE_DIR / stored_name
    stored_path.write_bytes(content)

    file_item = StoredFile(
        id=file_id,
        title=title,
        original_name=upload_file.filename or stored_name,
        stored_name=stored_name,
        mime_type=upload_file.content_type or mimetypes.guess_type(stored_name)[0] or "application/octet-stream",
        size=len(content),
        processing_status=ProcessingStatus.UPLOADED,
    )

    session.add(file_item)
    await session.commit()
    await session.refresh(file_item)

    process_scan_file_for_threats.delay(file_item.id)
    return Ok(file_item)

import uuid

from sqlalchemy.ext.asyncio.session import AsyncSession
from src.files.model import ProcessingStatus, ScanStatus
from src.types import Result, Ok, Err
from pathlib import Path
from .get_file import get_file

SUSPICIOUS_EXTENSIONS = {".exe", ".bat", ".cmd", ".sh", ".js"}
FILE_SIZE_LIMIT = 10 * 1024 * 1024 # 10 MB
PDF_MIME_TYPES = {"application/pdf", "application/octet-stream"}
PDF_EXT = ".pdf"

async def scan_file_for_threats(session: AsyncSession, file_id: uuid.UUID) -> Result[list[str]]:
    file_item_result = await get_file(session=session, file_id=file_id)
    if isinstance(file_item_result, Err):
        return file_item_result

    file_item = file_item_result.value
    file_item.processing_status = ProcessingStatus.PROCESSING
    await session.commit()

    reasons: list[str] = []
    extension = Path(file_item.original_name).suffix.lower()

    if extension in SUSPICIOUS_EXTENSIONS:
        reasons.append(f"suspicious extension {extension}")

    if file_item.size > FILE_SIZE_LIMIT:
        reasons.append("file is larger than 10 MB")

    if extension == PDF_EXT and file_item.mime_type not in PDF_MIME_TYPES:
        reasons.append("pdf extension does not match mime type")

    file_item.scan_status = ScanStatus.SUSPICIOUS if reasons else ScanStatus.CLEAN
    file_item.scan_details = ", ".join(reasons) if reasons else "no threats found"
    file_item.requires_attention = bool(reasons)
    await session.commit()
    return Ok(reasons)

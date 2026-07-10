import re
import uuid

from sqlalchemy.ext.asyncio.session import AsyncSession
from src.files.model import ProcessingStatus, ScanStatus
from src.types import Result, Ok, Err
from .get_file_and_path import get_file_and_path
from pathlib import Path

_LINE_BREAK_RE = re.compile(r'\r\n?|\n')

async def extract_file_metadata(session: AsyncSession, file_id: uuid.UUID) -> Result[dict[str, Unknown]]:
    get_file_and_path_result = await get_file_and_path(session, file_id)
    if isinstance(get_file_and_path_result, Err):
        return get_file_and_path_result

    file_item, stored_path = get_file_and_path_result.value
    if not stored_path.exists():
        scan_details = "Stored file not found during metadata extraction"
        file_item.processing_status = ProcessingStatus.FAILED
        file_item.scan_status = file_item.scan_status or ScanStatus.FAILED
        file_item.scan_details = scan_details
        await session.commit()
        return Err(scan_details)

    metadata = {
        "extension": Path(file_item.original_name).suffix.lower(),
        "size_bytes": file_item.size,
        "mime_type": file_item.mime_type,
    }

    if file_item.mime_type.startswith("text/"):
        content = stored_path.read_text(encoding="utf-8", errors="ignore")
        metadata["line_count"] = _count_lines(content)
        metadata["char_count"] = len(content)
    elif file_item.mime_type == "application/pdf":
        content = stored_path.read_bytes()
        metadata["approx_page_count"] = max(content.count(b"/Type /Page"), 1)

    file_item.metadata_json = metadata
    file_item.processing_status = ProcessingStatus.PROCESSED
    await session.commit()
    return Ok(metadata)

def _count_lines(text: str) -> int:
    if not text:
        return 0

    return sum(1 for _ in _LINE_BREAK_RE.finditer(text))

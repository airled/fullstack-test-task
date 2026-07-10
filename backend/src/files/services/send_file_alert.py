import uuid

from sqlalchemy.ext.asyncio.session import AsyncSession
from src.files.model import ProcessingStatus
from src.types import Result, Ok, Err
from src.alerts.model import Alert, Level
from .get_file import get_file

async def send_file_alert(session: AsyncSession, file_id: uuid.UUID) -> Result[Alert]:
    file_item_result = await get_file(session, file_id)
    if isinstance(file_item_result, Err):
        return file_item_result

    file_item = file_item_result.value
    if file_item.processing_status == ProcessingStatus.FAILED:
        alert = Alert(file_id=file_id, level=Level.CRITICAL, message="File processing failed")
    elif file_item.requires_attention:
        alert = Alert(
            file_id=file_id,
            level=Level.WARNING,
            message=f"File requires attention: {file_item.scan_details}",
        )
    else:
        alert = Alert(file_id=file_id, level=Level.INFO, message="File processed successfully")

    session.add(alert)
    await session.commit()
    return Ok(alert)

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.types import Result, Ok
from src.alerts.model import Alert

async def list_alerts(session: AsyncSession, offset: int, limit: int) -> Result[list[Alert]]:
    result = await session.execute(
        select(Alert).order_by(Alert.created_at.desc()).offset(offset).limit(limit)
    )
    return Ok(list(result.scalars().all()))

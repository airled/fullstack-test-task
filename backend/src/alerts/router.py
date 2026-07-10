from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db import get_db
from fastapi import APIRouter, Depends
from src.alerts.schemas import AlertItem
from src.alerts.services import list_alerts
from src.types import Err

router = APIRouter()

@router.get("/alerts", response_model=list[AlertItem])
async def list_alerts_view(
    offset: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_db),
):
    list_alerts_result = await list_alerts(session=session, offset=offset, limit=limit)
    if isinstance(list_alerts_result, Err):
        return []

    return list_alerts_result.value

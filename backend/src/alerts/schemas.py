import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.alerts.model import Level

class AlertItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_id: uuid.UUID
    level: Level
    message: str
    created_at: datetime

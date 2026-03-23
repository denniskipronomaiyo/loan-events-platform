from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class LoanEventResponse(BaseModel):
    event_id: UUID
    application_id: UUID
    event_type: str
    timestamp: datetime

    class Config:
        from_attributes = True
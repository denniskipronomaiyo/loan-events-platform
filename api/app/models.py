from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base


class LoanEvent(Base):
    __tablename__ = "loan_events"

    event_id = Column(UUID(as_uuid=True), primary_key=True)
    application_id = Column(UUID(as_uuid=True), ForeignKey("loan_applications.application_id"))
    event_type = Column(String, nullable=False)
    event_timestamp = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
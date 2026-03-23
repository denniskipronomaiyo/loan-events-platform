from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from ..database import get_db
from ..schemas import LoanEventResponse
from ..services.loan_event_service import get_events_by_application

router = APIRouter()


@router.get("/loan-applications/{application_id}/events", response_model=list[LoanEventResponse])
def fetch_loan_events(application_id: UUID, db: Session = Depends(get_db)):
    events = get_events_by_application(db, application_id)

    if not events:
        raise HTTPException(status_code=404, detail="No events found")

    return [
        LoanEventResponse(
            event_id=e.event_id,
            application_id=e.application_id,
            event_type=e.event_type,
            timestamp=e.event_timestamp
        )
        for e in events
    ]
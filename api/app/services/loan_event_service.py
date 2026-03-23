from sqlalchemy.orm import Session
from ..models import LoanEvent


def get_events_by_application(db: Session, application_id):
    return (
        db.query(LoanEvent)
        .filter(LoanEvent.application_id == application_id)
        .order_by(LoanEvent.event_timestamp.asc())
        .all()
    )
import redis
import json
import uuid
from datetime import datetime

r = redis.Redis(host="redis", port=6379, decode_responses=True)

QUEUE_NAME = "loan_events"


def produce_event(application_id, event_type):
    event = {
        "event_id": str(uuid.uuid4()),
        "application_id": application_id,
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat()
    }

    r.lpush(QUEUE_NAME, json.dumps(event))
    print("Produced:", event)


if __name__ == "__main__":
    # replace with real application_id from DB
    app_id = "00000000-0000-0000-0000-000000000006"

    produce_event(app_id, "submitted")
    produce_event(app_id, "approved")
    produce_event(app_id, "disbursed")
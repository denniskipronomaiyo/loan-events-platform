import os
import time
import psycopg2
from datetime import datetime
import uuid
import random

DATABASE_URL = os.getenv("DATABASE_URL")

EVENT_TYPES = ["submitted", "approved", "disbursed", "repaid", "defaulted"]


def insert_event():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT application_id FROM loan_applications LIMIT 1")
    result = cur.fetchone()
    application_id = result[0] if result else None

    if not application_id:
        print("No loan applications found.")
        return

    event_type = random.choice(EVENT_TYPES)

    cur.execute("""
        INSERT INTO loan_events (
            event_id,
            application_id,
            event_type,
            event_timestamp
        )
        VALUES (%s, %s, %s, %s)
    """, (
        str(uuid.uuid4()),
        application_id,
        event_type,
        datetime.utcnow()
    ))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Inserted event: {event_type}")


if __name__ == "__main__":
    while True:
        try:
            insert_event()
            time.sleep(5)
        except Exception as e:
            print("Error:", e)
            time.sleep(5)
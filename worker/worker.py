import redis
import json
import time
import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

r = redis.Redis(host="redis", port=6379, decode_responses=True)

QUEUE_NAME = "loan_events"
DLQ_NAME = "loan_events_dlq"


def insert_event(event):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO loan_events (
                event_id,
                application_id,
                event_type,
                event_timestamp
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (event_id) DO NOTHING
        """, (
            event["event_id"],
            event["application_id"],
            event["event_type"],
            event["timestamp"]
        ))

        conn.commit()

    finally:
        cur.close()
        conn.close()


def process_event(event_json):
    event = json.loads(event_json)

    # basic validation
    required_fields = ["event_id", "application_id", "event_type", "timestamp"]
    for field in required_fields:
        if field not in event:
            raise ValueError(f"Missing field: {field}")

    insert_event(event)


def handle_failure(event_json, attempt):
    if attempt >= 3:
        print("Sending to DLQ:", event_json)
        r.lpush(DLQ_NAME, event_json)
    else:
        time.sleep(2 ** attempt)
        r.lpush(QUEUE_NAME, event_json)


def worker_loop():
    print("Worker started...")

    while True:
        try:
            # blocking pop (waits for event)
            _, event_json = r.brpop(QUEUE_NAME)

            for attempt in range(3):
                try:
                    process_event(event_json)
                    print("Processed:", event_json)
                    break
                except Exception as e:
                    print(f"Error (attempt {attempt+1}):", e)
                    handle_failure(event_json, attempt)

        except Exception as e:
            print("Worker crash:", e)
            time.sleep(5)


if __name__ == "__main__":
    worker_loop()
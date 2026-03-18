from fastapi import FastAPI
import os
import psycopg2

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/loan-applications/{application_id}/events")
def get_loan_events(application_id: str):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        SELECT event_id, application_id, event_type, event_timestamp
        FROM loan_events
        WHERE application_id = %s
        ORDER BY event_timestamp ASC
    """, (application_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "event_id": str(r[0]),
            "application_id": str(r[1]),
            "event_type": r[2],
            "timestamp": r[3]
        }
        for r in rows
    ]
from fastapi import FastAPI
from .routes import loan_events

app = FastAPI()

app.include_router(loan_events.router)


@app.get("/")
def health():
    return {"status": "ok"}
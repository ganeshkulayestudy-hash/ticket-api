from fastapi import FastAPI

from routes import router
from storage import tickets  # noqa: F401  (tests import tickets from here)

app = FastAPI(title="Ticket API")
app.include_router(router)


@app.get("/")
def home():
    return {"message": "Ticket API is running"}

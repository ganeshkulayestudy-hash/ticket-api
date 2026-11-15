from fastapi import FastAPI

from config import settings
from routes import router
from storage import tickets  # noqa: F401  (tests import tickets from here)

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(router)


@app.get("/")
def home():
    return {"message": f"{settings.app_name} is running"}

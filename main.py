import logging

from fastapi import FastAPI

from config import settings
from errors import register_error_handlers
from routes import router
from storage import tickets  # noqa: F401  (tests import tickets from here)

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(title=settings.app_name, debug=settings.debug)
register_error_handlers(app)
app.include_router(router)


@app.get("/")
def home():
    return {"message": f"{settings.app_name} is running"}

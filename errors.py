import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("ticket_api")


def error_body(code, message, details=None):
    body = {"error": {"code": code, "message": message}}
    if details:
        body["error"]["details"] = details
    return body


def register_error_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):
        logger.warning("%s %s -> %s %s", request.method, request.url.path, exc.status_code, exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content=error_body(exc.status_code, str(exc.detail)),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        details = [
            {"field": ".".join(str(part) for part in e["loc"][1:]), "message": e["msg"]}
            for e in exc.errors()
        ]
        logger.warning("%s %s -> 422 validation failed", request.method, request.url.path)
        return JSONResponse(
            status_code=422,
            content=error_body(422, "Validation failed", details),
        )

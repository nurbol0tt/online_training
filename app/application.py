from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker
from starlette.exceptions import HTTPException

from app.controller.http.v1 import health
from fastapi import FastAPI

from app.controller.http.v1.routes import user
from app.utils.exception.exception_handlers import ExceptionHandlers
from app.utils.exception.exception_types import DataException, ServiceException


def create_app():
    app = FastAPI(
        title="FastAPI Pydiator",
        description="FastAPI pydiator integration project",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/",
        redoc_url="/redoc"
    )

    app.add_exception_handler(Exception, ExceptionHandlers.unhandled_exception)
    app.add_exception_handler(DataException, ExceptionHandlers.data_exception)
    app.add_exception_handler(ServiceException, ExceptionHandlers.service_exception)
    app.add_exception_handler(HTTPException, ExceptionHandlers.http_exception)
    app.add_exception_handler(ValidationError, ExceptionHandlers.validation_exception)

    app.include_router(health.router)
    app.include_router(user.router)

    return app

from pydantic import ValidationError
from starlette.exceptions import HTTPException

from fastapi import FastAPI

from app.utils.exception.exception_handlers import ExceptionHandlers
from app.utils.exception.exception_types import DataException, ServiceException
from app.api.v1.routes import routers as v1_routers


def create_app():
    app = FastAPI(
        title="FastAPI COURSE",
        description="FastAPI course integration project",
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

    app.include_router(v1_routers)

    return app

import logging

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger("shopsphere")


async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    request_id = getattr(request.state, "request_id", "unknown")

    logger.warning(
        "HTTP error | request_id=%s | path=%s | status=%s",
        request_id,
        request.url.path,
        exc.status_code
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": str(exc.detail),
                "request_id": request_id
            }
        },
        headers=exc.headers
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    request_id = getattr(request.state, "request_id", "unknown")

    logger.warning(
        "Validation error | request_id=%s | path=%s",
        request_id,
        request.url.path
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": 422,
                "message": "Input validation failed",
                "details": exc.errors(),
                "request_id": request_id
            }
        }
    )


async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError
):
    request_id = getattr(request.state, "request_id", "unknown")

    logger.exception(
        "Database error | request_id=%s | path=%s",
        request_id,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "A database error occurred",
                "request_id": request_id
            }
        }
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
):
    request_id = getattr(request.state, "request_id", "unknown")

    logger.exception(
        "Unexpected application error | request_id=%s | path=%s",
        request_id,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "request_id": request_id
            }
        }
    )

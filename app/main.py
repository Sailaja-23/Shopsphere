import logging
import time
import uuid

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api.products import router as product_router
from app.api.customers import router as customer_router
from app.api.orders import router as order_router

from app.db.database import Base, engine

from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem

from app.core.logging_config import setup_logging

from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    general_exception_handler
)


# Configure application logging
setup_logging()

logger = logging.getLogger("shopsphere")


# Register database models and create tables



app = FastAPI(
    title="ShopSphere API",
    description="E-commerce Order Management System",
    version="1.0.0"
)


# Register centralized exception handlers
app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    try:
        response = await call_next(request)

        duration = round(
            (time.time() - start_time) * 1000,
            2
        )

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request completed | request_id=%s | method=%s "
            "| path=%s | status=%s | duration_ms=%s",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration
        )

        return response

    except Exception:
        logger.exception(
            "Request failed | request_id=%s | method=%s | path=%s",
            request_id,
            request.method,
            request.url.path
        )
        raise


@app.get("/")
def home():
    return {
        "message": "Welcome to ShopSphere!",
        "status": "Application is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/about")
def about():
    return {
        "application": "ShopSphere",
        "purpose": "E-commerce Order Management",
        "framework": "FastAPI"
    }


# Register API routers
app.include_router(product_router)
app.include_router(customer_router)
app.include_router(order_router)


@app.on_event("startup")
async def startup_event():
    logger.info("ShopSphere application started")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("ShopSphere application stopped")

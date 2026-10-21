import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ImageNotFoundError,
    StorageError,
    StorageUnavailableError,
)
from app.services.exceptions import ProductNotFoundError


logger = logging.getLogger(__name__)


async def product_not_found_handler(
    request: Request,
    error: ProductNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Product not found"},
    )


async def image_not_found_handler(
    request: Request,
    error: ImageNotFoundError,
) -> JSONResponse:
    logger.error(
        "Image is missing: method=%s path=%s",
        request.method,
        request.url.path,
        exc_info=(type(error), error, error.__traceback__),
    )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Image not found"},
    )


async def storage_unavailable_handler(
    request: Request,
    error: StorageUnavailableError,
) -> JSONResponse:
    logger.error(
        "Storage is unavailable: method=%s path=%s",
        request.method,
        request.url.path,
        exc_info=(type(error), error, error.__traceback__),
    )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Image storage is temporarily unavailable"},
    )


async def storage_error_handler(
    request: Request,
    error: StorageError,
) -> JSONResponse:
    logger.error(
        "Storage operation failed: method=%s path=%s",
        request.method,
        request.url.path,
        exc_info=(type(error), error, error.__traceback__),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Image storage operation failed"},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        ProductNotFoundError,
        product_not_found_handler,
    )
    app.add_exception_handler(
        ImageNotFoundError,
        image_not_found_handler,
    )
    app.add_exception_handler(
        StorageUnavailableError,
        storage_unavailable_handler,
    )
    app.add_exception_handler(
        StorageError,
        storage_error_handler,
    )
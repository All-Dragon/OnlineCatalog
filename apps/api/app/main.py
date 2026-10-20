import logging
from asyncio import to_thread
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.s3 import create_s3_client, ensure_bucket
from app.db.session import engine
from app.routers.products import products_router


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging(settings)
    logger.info("Starting API")

    try:
        s3_client = await to_thread(create_s3_client, settings)

        try:
            await to_thread(
                ensure_bucket,
                s3_client,
                settings.s3_bucket_name,
            )

            app.state.s3_client = s3_client
            logger.info("API resources initialized")
            yield
        finally:
            await to_thread(s3_client.close)
    finally:
        await engine.dispose()
        logger.info("API resources released")


app = FastAPI(lifespan=lifespan)
app.include_router(products_router, prefix="/api/v1")

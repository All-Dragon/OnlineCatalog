import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from aiogram import Bot
from fastapi import FastAPI
from httpx import AsyncClient, Timeout

from app.clients.catalog import CatalogClient
from app.core.config import settings
from app.core.logging import configure_logging
from app.routers.webhook import webhook_router


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging(settings)
    logger.info("Starting bot application")

    bot = Bot(
        token=settings.telegram_bot_token.get_secret_value(),
    )

    try:
        async with AsyncClient(
            base_url=str(settings.api_base_url),
            headers={
                "X-Service-Token": (
                    settings.api_service_token.get_secret_value()
                ),
            },
            timeout=Timeout(20.0, connect=5.0),
        ) as http_client:
            app.state.bot = bot
            app.state.catalog_client = CatalogClient(http_client)

            logger.info("Bot resources initialized")

            yield
    finally:
        await bot.session.close()
        logger.info("Bot resources released")


app = FastAPI(lifespan=lifespan)
app.include_router(webhook_router)

import logging
from secrets import compare_digest
from typing import Annotated, Any

from aiogram import Bot
from aiogram.types import Update
from fastapi import (
    APIRouter,
    Body,
    Depends,
    Header,
    HTTPException,
    Request,
    status,
)
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.core.config import settings
from app.dispatcher import dispatcher


logger = logging.getLogger(__name__)


webhook_router = APIRouter(prefix="/telegram")


async def require_webhook_secret(
    secret: Annotated[
        str | None,
        Header(alias="X-Telegram-Bot-Api-Secret-Token"),
    ] = None,
) -> None:
    expected = settings.telegram_webhook_secret.get_secret_value()

    if secret is None or not compare_digest(
        secret.encode("utf-8"),
        expected.encode("utf-8"),
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid webhook credentials",
        )


async def parse_update(
    payload: Annotated[
        dict[str, Any],
        Body(examples=[{"update_id": 1}]),
    ],
) -> Update:
    try:
        return Update.model_validate(payload)
    except ValidationError as error:
        errors = [
            {
                **item,
                "loc": ("body", *item["loc"]),
            }
            for item in error.errors()
        ]
        raise RequestValidationError(errors) from error


@webhook_router.post(
    "/webhook",
    dependencies=[Depends(require_webhook_secret)],
)
async def receive_update(
    update: Annotated[Update, Depends(parse_update)],
    request: Request,
) -> dict[str, bool]:
    bot: Bot = request.app.state.bot

    logger.debug("Received Telegram update: update_id=%s", update.update_id)

    await dispatcher.feed_update(
        bot,
        update,
        catalog_client=request.app.state.catalog_client,
    )

    logger.debug("Processed Telegram update: update_id=%s", update.update_id)

    return {"ok": True}

import logging

from httpx import AsyncClient

from app.schemas.product import ProductRead


logger = logging.getLogger(__name__)


class CatalogClient:
    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def create_product(
        self,
        *,
        title: str,
        source_chat_id: int,
        source_message_id: int,
        photo: bytes,
    ) -> ProductRead:
        response = await self._client.post(
            "/api/v1/products",
            data={
                "title": title,
                "source_chat_id": str(source_chat_id),
                "source_message_id": str(source_message_id),
            },
            files={
                "photo": (
                    "product.jpg",
                    photo,
                    "image/jpeg",
                ),
            },
        )

        response.raise_for_status()

        product = ProductRead.model_validate(response.json())

        logger.debug(
            "API returned product: product_id=%s chat_id=%s message_id=%s",
            product.id,
            source_chat_id,
            source_message_id,
        )

        return product

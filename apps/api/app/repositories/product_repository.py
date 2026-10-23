from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.db.models.product import Product


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_products(self) -> list[Product]:
        result = await self._session.scalars(
            select(Product).order_by(Product.created_at.desc())
        )
        return list(result.all())

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self._session.get(Product, product_id)

    async def get_by_source_message(
        self,
        source_chat_id: int,
        source_message_id: int,
    ) -> Product | None:
        return await self._session.scalar(
            select(Product).where(
                Product.source_chat_id == source_chat_id,
                Product.source_message_id == source_message_id,
            )
        )

    async def create_if_absent(
        self,
        *,
        title: str,
        image_key: str,
        source_chat_id: int,
        source_message_id: int,
    ) -> Product | None:
        statement = (
            insert(Product)
            .values(
                title=title,
                image_key=image_key,
                source_chat_id=source_chat_id,
                source_message_id=source_message_id,
            )
            .on_conflict_do_nothing()
            .returning(Product)
        )

        return await self._session.scalar(statement)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_products(self) -> list[Product]:
        result = await self._session.scalars(
            select(Product).order_by(Product.created_at.desc())
        )
        return list(result.all())

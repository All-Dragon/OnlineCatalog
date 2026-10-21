import logging
from hashlib import sha256

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.image_repository import ImageData, ImageRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductRead
from app.services.exceptions import ProductNotFoundError


logger = logging.getLogger(__name__)


class ProductService:
    def __init__(
        self,
        session: AsyncSession,
        product_repository: ProductRepository,
        image_repository: ImageRepository,
    ) -> None:
        self._session = session
        self._product_repository = product_repository
        self._image_repository = image_repository

    async def list_products(self) -> list[ProductRead]:
        products = await self._product_repository.list_products()

        logger.debug("Listed products: count=%s", len(products))

        return [
            ProductRead(
                id=product.id,
                title=product.title,
                image_url=f"/api/v1/products/{product.id}/image",
            )
            for product in products
        ]

    async def get_image(self, product_id: int) -> ImageData:
        product = await self._product_repository.get_by_id(product_id)

        if product is None:
            logger.debug("Product not found: product_id=%s", product_id)
            raise ProductNotFoundError(product_id)

        logger.debug(
            "Resolved product image: product_id=%s key=%s",
            product_id,
            product.image_key,
        )

        return await self._image_repository.download(product.image_key)

    async def create_product(
        self,
        data: ProductCreate,
        image: ImageData,
    ) -> ProductRead:
        created = False

        async with self._session.begin():
            product = await self._product_repository.get_by_source_message(
                source_chat_id=data.source_chat_id,
                source_message_id=data.source_message_id,
            )

            if product is None:
                digest = sha256(image.data).hexdigest()
                image_key = (
                    f"products/telegram/{data.source_chat_id}/"
                    f"{data.source_message_id}/{digest}"
                )

                product = await self._product_repository.create_if_absent(
                    title=data.title,
                    image_key=image_key,
                    source_chat_id=data.source_chat_id,
                    source_message_id=data.source_message_id,
                )

                if product is not None:
                    await self._image_repository.upload(
                        key=image_key,
                        data=image.data,
                        content_type=image.content_type,
                    )
                    created = True
                else:
                    product = (
                        await self._product_repository.get_by_source_message(
                            source_chat_id=data.source_chat_id,
                            source_message_id=data.source_message_id,
                        )
                    )

                    if product is None:
                        raise RuntimeError(
                            "Product not found after source message conflict"
                        )

        if created:
            logger.info("Created product: product_id=%s", product.id)
        else:
            logger.debug("Reused product: product_id=%s", product.id)

        return ProductRead(
            id=product.id,
            title=product.title,
            image_url=f"/api/v1/products/{product.id}/image",
        )

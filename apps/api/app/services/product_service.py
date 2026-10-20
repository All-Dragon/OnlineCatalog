import logging

from app.repositories.image_repository import ImageData, ImageRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductRead
from app.services.exceptions import ProductNotFoundError


logger = logging.getLogger(__name__)


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository,
        image_repository: ImageRepository,
    ) -> None:
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

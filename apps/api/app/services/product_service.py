from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductRead


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    async def list_products(self) -> list[ProductRead]:
        products = await self._repository.list_products()

        return [
            ProductRead(
                id=product.id,
                title=product.title,
                image_url=f"/api/v1/products/{product.id}/image",
            )
            for product in products
        ]

from fastapi import APIRouter

from app.api.dependencies import ProductServiceDep
from app.schemas.product import ProductRead


products_router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@products_router.get("", response_model=list[ProductRead])
async def list_products(
    service: ProductServiceDep,
) -> list[ProductRead]:
    return await service.list_products()

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Response, status

from app.api.dependencies import ProductServiceDep
from app.schemas.product import ProductRead
from app.services.exceptions import ProductNotFoundError


products_router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@products_router.get("", response_model=list[ProductRead])
async def list_products(
    service: ProductServiceDep,
) -> list[ProductRead]:
    return await service.list_products()


@products_router.get("/{product_id}/image", response_class=Response)
async def get_product_image(
    product_id: Annotated[int, Path(gt=0)],
    service: ProductServiceDep,
) -> Response:
    try:
        image = await service.get_image(product_id)
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        ) from error

    return Response(
        content=image.data,
        media_type=image.content_type,
    )

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Path,
    Response,
    UploadFile,
)

from app.api.dependencies import (
    ProductCreateDep,
    ProductServiceDep,
    require_service_token,
)
from app.api.uploads import read_product_image
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


@products_router.get("/{product_id}/image", response_class=Response)
async def get_product_image(
    product_id: Annotated[int, Path(gt=0)],
    service: ProductServiceDep,
) -> Response:
    image = await service.get_image(product_id)

    return Response(
        content=image.data,
        media_type=image.content_type,
    )


@products_router.post(
    "",
    response_model=ProductRead,
    dependencies=[Depends(require_service_token)],
)
async def create_product(
    service: ProductServiceDep,
    data: ProductCreateDep,
    photo: Annotated[UploadFile, File()],
) -> ProductRead:
    image = await read_product_image(photo)

    return await service.create_product(
        data=data,
        image=image,
    )

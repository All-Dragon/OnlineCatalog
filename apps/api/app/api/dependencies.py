from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.repositories.image_repository import ImageRepository
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService


SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_image_repository(request: Request) -> ImageRepository:
    return ImageRepository(
        client=request.app.state.s3_client,
        bucket_name=settings.s3_bucket_name,
    )


ImageRepositoryDep = Annotated[ImageRepository, Depends(get_image_repository)]


def get_product_repository(session: SessionDep) -> ProductRepository:
    return ProductRepository(session)


ProductRepositoryDep = Annotated[ProductRepository, Depends(get_product_repository)]


def get_product_service(
    image_repository: ImageRepositoryDep,
    product_repository: ProductRepositoryDep,
) -> ProductService:
    return ProductService(
        product_repository=product_repository,
        image_repository=image_repository,
    )


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]

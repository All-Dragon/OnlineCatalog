from secrets import compare_digest
from typing import Annotated

from fastapi import Depends, Form, Header, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.repositories.image_repository import ImageRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate
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
    session: SessionDep,
    image_repository: ImageRepositoryDep,
    product_repository: ProductRepositoryDep,
) -> ProductService:
    return ProductService(
        session=session,
        product_repository=product_repository,
        image_repository=image_repository,
    )


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]


async def require_service_token(
    service_token: Annotated[
        str | None,
        Header(alias="X-Service-Token"),
    ] = None,
) -> None:
    expected_token = settings.api_service_token.get_secret_value()

    if service_token is None or not compare_digest(
        service_token.encode("utf-8"),
        expected_token.encode("utf-8"),
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid service credentials",
        )


async def get_product_create(
    title: Annotated[str, Form()],
    source_chat_id: Annotated[int, Form()],
    source_message_id: Annotated[int, Form()],
) -> ProductCreate:
    try:
        return ProductCreate(
            title=title,
            source_chat_id=source_chat_id,
            source_message_id=source_message_id,
        )
    except ValidationError as error:
        errors = [
            {
                **item,
                "loc": ("body", *item["loc"]),
            }
            for item in error.errors()
        ]
        raise RequestValidationError(errors) from error


ProductCreateDep = Annotated[ProductCreate, Depends(get_product_create)]

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService


SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_product_service(session: SessionDep) -> ProductService:
    repository = ProductRepository(session)
    return ProductService(repository)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]

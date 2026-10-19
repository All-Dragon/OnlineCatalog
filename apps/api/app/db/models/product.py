from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Identity, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(Text, nullable=False)

    image_key: Mapped[str] = mapped_column(Text, nullable=False)

    source_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    source_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "image_key",
            name="uq_products_image_key",
        ),
        UniqueConstraint(
            "source_chat_id",
            "source_message_id",
            name="uq_products_source_message",
        )
    )

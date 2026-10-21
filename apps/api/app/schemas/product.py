from pydantic import BaseModel, Field, field_validator


class ProductRead(BaseModel):
    id: int
    title: str
    image_url: str


class ProductCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    source_chat_id: int = Field(
        ge=-(2**63),
        le=2**63 - 1,
    )
    source_message_id: int = Field(
        gt=0,
        le=2**63 - 1,
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        title = value.strip()

        if not title:
            raise ValueError("Title must not be blank")

        return title

    @field_validator("source_chat_id")
    @classmethod
    def validate_source_chat_id(cls, value: int) -> int:
        if value == 0:
            raise ValueError("Source chat ID must not be zero")

        return value

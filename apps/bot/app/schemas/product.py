from pydantic import BaseModel, Field


class ProductRead(BaseModel):
    id: int = Field(gt=0)
    title: str
    image_url: str

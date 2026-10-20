from pydantic import BaseModel


class ProductRead(BaseModel):
    id: int
    title: str
    image_url: str
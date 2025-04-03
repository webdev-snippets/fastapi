import uuid
from sqlmodel import SQLModel, Field, String, JSON
from pydantic import UUID4
from typing import Optional, Literal, List


class BaseProduct(SQLModel):
    title: str
    description: str
    tags: List[str] = Field(sa_type=JSON)
    image_path: str


class Product(BaseProduct, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)


class CreateProduct(BaseProduct):
    pass


class PublicProduct(BaseProduct):
    id: UUID4


class UpdateProduct(SQLModel):
    title: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    image_path: Optional[str]

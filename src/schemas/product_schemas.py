from pydantic import BaseModel, ConfigDict
from sqlsqlalchemy import UUID


class ProductBase(BaseModel):
    name: str
    price: float
    description: str
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

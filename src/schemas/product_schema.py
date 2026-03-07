"""
Esquemas Pydantic para el recurso de productos.

Incluye ProductBase, ProductCreate, ProductUpdate, ProductResponse,
ProductCategoriesUpdate y referencias DiscountRef, CategoryRef.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class DiscountRef(BaseModel):
    """Referencia mínima de descuento para incluir en Product (id, code, value)."""

    id: UUID
    code: str
    value: Decimal
    status: str
    model_config = ConfigDict(from_attributes=True)


class CategoryRef(BaseModel):
    """Referencia mínima de categoría para incluir en Product (id, name)."""

    id: UUID
    name: str
    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    """Campos base de producto: nombre, precio, descripción, stock."""

    name: str
    price: Decimal
    description: str | None = None
    stock: int = 0


class ProductCreate(ProductBase):
    """Esquema para crear producto; añade id_discount y category_ids opcionales."""

    id_discount: UUID | None = None
    category_ids: list[UUID] | None = None


class ProductUpdate(BaseModel):
    """Esquema para actualización parcial de producto."""

    name: str | None = None
    price: Decimal | None = None
    description: str | None = None
    stock: int | None = None
    id_discount: UUID | None = None


class ProductCategoriesUpdate(BaseModel):
    """Body para asignar/actualizar categorías de un producto (lista de UUIDs)."""

    category_ids: list[UUID]


class ProductResponse(ProductBase):
    """Respuesta de producto con id, id_discount, discount (ref), categorías."""

    id: UUID
    id_discount: UUID | None = None
    discount: DiscountRef | None = None
    categories: list[CategoryRef] = []

    model_config = ConfigDict(from_attributes=True)

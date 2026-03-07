"""
Esquemas Pydantic para el recurso de categorías.

Incluye CategoryBase, CategoryCreate, CategoryUpdate y CategoryResponse.
"""

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class CategoryBase(BaseModel):
    """Campos base de categoría: nombre."""

    name: str


class CategoryCreate(CategoryBase):
    """Esquema para crear una categoría."""

    pass


class CategoryUpdate(BaseModel):
    """Esquema para actualización parcial de categoría."""

    name: str | None = None


class CategoryResponse(CategoryBase):
    """Respuesta de categoría con id."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)

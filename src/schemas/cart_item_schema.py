"""
Esquemas Pydantic para CartItem.

CartItemCreate, CartItemUpdate, CartItemResponse y CartItemDetailResponse
(con usuario y producto anidados para lecturas detalladas).
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from src.schemas.product_schema import ProductResponse
from src.schemas.user_schema import UserResponse


class CartItemBase(BaseModel):
    """Campos comunes: cantidad en el carrito."""

    quantity: PositiveInt = Field(..., description="Cantidad del producto en el carrito")


class CartItemCreate(CartItemBase):
    """Crear línea de carrito; usuario opcional (FK nullable en BD)."""

    id_user: UUID | None = Field(None, description="ID del usuario propietario del carrito")
    id_product: UUID = Field(..., description="ID del producto")


class CartItemUpdate(BaseModel):
    """Actualización parcial: cantidad y/o usuario asociado."""

    quantity: PositiveInt | None = Field(None, description="Nueva cantidad")
    id_user: UUID | None = Field(None, description="Usuario propietario (null = anónimo)")


class CartItemResponse(CartItemBase):
    """Respuesta estándar con IDs."""

    id: UUID = Field(..., description="ID único del artículo del carrito")
    id_user: UUID | None = Field(None, description="ID del usuario propietario")
    id_product: UUID = Field(..., description="ID del producto")

    model_config = ConfigDict(from_attributes=True)


class CartItemDetailResponse(CartItemResponse):
    """Respuesta con relaciones N:1 cargadas (user, product)."""

    user: UserResponse | None = None
    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)

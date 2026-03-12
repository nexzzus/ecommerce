"""

Esquemas Pydantic para el recurso de descuentos.

Incluye DiscountBase, DiscountCreate, DiscountUpdate y DiscountResponse.

"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from uuid import UUID


class DiscountBase(BaseModel):
    """Campos base de descuento: valor, código y estado."""

    value: Decimal

    code: str

    status: str = "active"


class DiscountCreate(DiscountBase):
    """Esquema para crear un descuento."""

    pass


class DiscountUpdate(BaseModel):
    """Esquema para actualización parcial de descuento."""

    value: Decimal | None = None

    code: str | None = None

    status: str | None = None


class DiscountResponse(DiscountBase):
    """Respuesta de descuento con id."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)

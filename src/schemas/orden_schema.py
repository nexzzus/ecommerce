from datetime import date
from pydantic import BaseModel


class OrdenBase(BaseModel):
    fecha: date
    total: float


class OrdenCreate(OrdenBase):
    pass


class OrdenResponse(OrdenBase):
    id: int

    class Config:
        from_attributes = True

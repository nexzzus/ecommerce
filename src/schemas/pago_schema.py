from pydantic import BaseModel
from datetime import date

class PagoBase(BaseModel):
    fecha_pago: date
    monto: float
    metodo_pago: str
    orden_id: int

class PagoCreate(PagoBase):
    pass

class PagoResponse(PagoBase):
    id: int

class Config:
    from_attributes = True
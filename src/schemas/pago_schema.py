from pydantic import BaseModel


class PagoBase(BaseModel):
    metodo: str
    monto: float
    orden_id: int


class PagoCreate(PagoBase):
    pass


class PagoResponse(PagoBase):
    id: int

    class Config:
        from_attributes = True

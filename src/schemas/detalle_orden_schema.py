from pydantic import BaseModel

class DetalleOrdenBase(BaseModel):
    producto: str
    cantidad: int
    precio_unitario: float
    orden_id: int

class DetalleOrdenCreate(DetalleOrdenBase):
    pass

class DetalleOrdenResponse(DetalleOrdenBase):
    id: int

class Config:
    from_attributes = True
from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class OrdenBase(BaseModel):
    fecha: date
    total: float

class OrdenCreate(OrdenBase):
    pass

class OrdenResponse(OrdenBase):
    id: int

class Config:
    from_attributes = True
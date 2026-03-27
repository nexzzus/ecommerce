from sqlalchemy import Column, Integer, Date, Float
from sqlalchemy.orm import relationship
from ..database.database import Base

class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    total = Column(Float, nullable=False)
    
    detalles = relationship("DetalleOrden", back_populates="orden")
    pago = relationship("Pago", back_populates="orden", uselist=False)
from sqlalchemy import Column, Integer, Date, Float, String, DateTime  # <--- AGREGAMOS String Y DateTime
from sqlalchemy.orm import relationship
from ..database.database import Base


class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False) # Mantenlo como Date si tus compañeros ya lo tenían así
    total = Column(Float, nullable=False)
    
    
    estado = Column(String, default="Pendiente", nullable=False) 


    detalles = relationship("DetalleOrden", back_populates="orden")
    pago = relationship("Pago", back_populates="orden", uselist=False)
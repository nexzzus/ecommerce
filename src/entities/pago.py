from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database.database import Base


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    fecha_pago = Column(Date, nullable=False)
    monto = Column(Float, nullable=False)

    orden_id = Column(Integer, ForeignKey("ordenes.id"))
    orden = relationship("Orden", back_populates="pago")

"""
Modelo SQLAlchemy para la entidad Discount.

Descuento con valor, código y estado; los productos pueden referenciarlo (N:1).
"""

import uuid

from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Discount(Base):
    """
    Entidad descuento: valor (porcentaje o monto), código y estado (activo/inactivo).
    """

    __tablename__ = "discounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    value = Column(Numeric(10, 2), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    status = Column(String(20), nullable=False, default="active")

    products = relationship("Product", back_populates="discount")

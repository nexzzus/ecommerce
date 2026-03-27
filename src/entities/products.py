"""
Modelo SQLAlchemy para la entidad Product.

Producto con nombre, precio, descripción, stock; FK a Discount (opcional)
y relación N:M con Category (product_categories).
"""

import uuid

from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base
from src.entities.associations import product_categories


class Product(Base):
    """
    Entidad producto: nombre, precio, descripción, stock; descuento opcional y categorías N:M.
    """

    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_discount = Column(
        UUID(as_uuid=True),
        ForeignKey("discounts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    name = Column(String(200), nullable=False, index=True)
    price = Column(Numeric(12, 2), nullable=False)
    description = Column(String(1000), nullable=True)
    stock = Column(Integer, nullable=False, default=0)

    discount = relationship("Discount", back_populates="products")
    categories = relationship(
        "Category", secondary=product_categories, back_populates="products"
    )
    cart_items = relationship("CartItem", back_populates="product")

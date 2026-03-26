"""
Modelo SQLAlchemy para líneas del carrito.

Muchos cart_items → un User (N:1, opcional para carrito anónimo)
y muchos cart_items → un Product (N:1).
"""

import uuid

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class CartItem(Base):
    """Línea de carrito: usuario, producto y cantidad."""

    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    id_user = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    id_product = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    quantity = Column(Integer, nullable=False, default=0)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

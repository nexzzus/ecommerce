"""

Modelo SQLAlchemy para la entidad Category.

Categoría con nombre; relación N:M con productos (product_categories).

"""

import uuid

from sqlalchemy import Column, String

from sqlalchemy.dialects.postgresql.base import UUID

from sqlalchemy.orm import relationship

from src.database.config import Base

from src.entities.associations import product_categories


class Category(Base):
    """

    Entidad categoría: nombre y productos asociados (N:M).

    """

    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    name = Column(String(100), unique=True, index=True, nullable=False)

    products = relationship(
        "Product", secondary=product_categories, back_populates="categories"
    )

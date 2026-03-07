"""
Modelo SQLAlchemy para la entidad Role.

Rol con relación N:M a permisos (role_permissions) y a usuarios (user_roles).
"""
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base
from src.entities.associations import role_permissions, user_roles


class Role(Base):
    """
    Entidad rol: nombre y relaciones con permisos y usuarios.
    """

    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)

    permissions = relationship(
        "Permission", secondary=role_permissions, back_populates="roles"
    )
    users = relationship("User", secondary=user_roles, back_populates="roles")

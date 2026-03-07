import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base
from src.entities.associations import role_permissions


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(150), nullable=False)

    roles = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )
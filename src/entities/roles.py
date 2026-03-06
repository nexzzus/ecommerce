import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql.base import UUID

from src.database.config import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
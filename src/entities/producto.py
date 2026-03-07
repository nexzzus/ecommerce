from src.database.config import Base
from sqlalchemy import Column, String, Text, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Product(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(150), nullable=False, index=True)
    price = Column(Numeric(10, 2), nulable=False)
    description = Column(Text, nullable=True)
    stock = Column(Integer, nullable=False, default=0)

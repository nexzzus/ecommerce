from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    address: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    phone: str | None = None
    address: str | None = None

class UserResponse(UserBase):
    id: UUID
    date_created: datetime | None = None
    date_updated: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
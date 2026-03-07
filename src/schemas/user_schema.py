from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class RoleRef(BaseModel):
    """Referencia mínima de rol para incluir en User."""
    id: UUID
    name: str
    model_config = ConfigDict(from_attributes=True)


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


class UserRolesUpdate(BaseModel):
    """Body para asignar/actualizar roles de un usuario."""
    role_ids: list[UUID]


class UserResponse(UserBase):
    id: UUID
    date_created: datetime | None = None
    date_updated: datetime | None = None
    roles: list[RoleRef] = []

    model_config = ConfigDict(from_attributes=True)
"""
Esquemas Pydantic para el recurso de usuarios.

Incluye UserBase, UserCreate, UserUpdate, UserResponse, UserRolesUpdate
y RoleRef (referencia mínima de rol para incluir en respuestas).
"""
from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class RoleRef(BaseModel):
    """Referencia mínima de rol para incluir en User (id y name)."""

    id: UUID
    name: str
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    """Campos base de usuario: nombre, apellido, email, teléfono, dirección."""

    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    address: str | None = None


class UserCreate(UserBase):
    """Esquema para crear usuario; añade password y opcionalmente roles."""

    password: str
    role_ids: list[UUID] | None = None


class UserUpdate(BaseModel):
    """Esquema para actualización parcial de usuario (todos los campos opcionales)."""

    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    phone: str | None = None
    address: str | None = None


class UserRolesUpdate(BaseModel):
    """Body para asignar/actualizar roles de un usuario (lista de UUIDs)."""

    role_ids: list[UUID]


class UserResponse(UserBase):
    """Respuesta de usuario con id, fechas y lista de roles."""

    id: UUID
    date_created: datetime | None = None
    date_updated: datetime | None = None
    roles: list[RoleRef] = []

    model_config = ConfigDict(from_attributes=True)

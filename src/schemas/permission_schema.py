"""
Esquemas Pydantic para el recurso de permisos.

Incluye PermissionBase, PermissionCreate, PermissionUpdate y PermissionResponse.
"""

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class PermissionBase(BaseModel):
    """Campos base de permiso: nombre y descripción opcional."""

    name: str
    description: str | None = None


class PermissionCreate(PermissionBase):
    """Esquema para crear un permiso."""

    pass


class PermissionUpdate(BaseModel):
    """Esquema para actualización parcial de permiso."""

    name: str | None = None
    description: str | None = None


class PermissionResponse(PermissionBase):
    """Respuesta de permiso con id."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)

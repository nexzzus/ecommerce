"""
Esquemas Pydantic para el recurso de roles.

Incluye RoleBase, RoleCreate, RoleUpdate, RoleResponse, RolePermissionsUpdate
y PermissionRef (referencia mínima de permiso para incluir en respuestas).
"""
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class RoleBase(BaseModel):
    """Campos base de rol: nombre."""

    name: str


class RoleCreate(RoleBase):
    """Esquema para crear un rol."""

    pass


class RoleUpdate(BaseModel):
    """Esquema para actualización parcial de rol."""

    name: str | None = None


class RolePermissionsUpdate(BaseModel):
    """Body para asignar/actualizar permisos de un rol (lista de UUIDs)."""

    permission_ids: list[UUID]


class PermissionRef(BaseModel):
    """Referencia mínima de permiso para incluir en Role (id, name, description)."""

    id: UUID
    name: str
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)


class RoleResponse(RoleBase):
    """Respuesta de rol con id y lista de permisos."""

    id: UUID
    permissions: list[PermissionRef] = []

    model_config = ConfigDict(from_attributes=True)

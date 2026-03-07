from pydantic import BaseModel, ConfigDict
from uuid import UUID


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = None


class RolePermissionsUpdate(BaseModel):
    """Body para asignar/actualizar permisos de un rol."""
    permission_ids: list[UUID]


class PermissionRef(BaseModel):
    """Referencia mínima de permiso para incluir en Role."""
    id: UUID
    name: str
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)


class RoleResponse(RoleBase):
    id: UUID
    permissions: list[PermissionRef] = []

    model_config = ConfigDict(from_attributes=True)

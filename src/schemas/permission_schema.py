from pydantic import BaseModel, ConfigDict
from uuid import UUID


class PermissionBase(BaseModel):
    name: str
    description: str | None = None


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class PermissionResponse(PermissionBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

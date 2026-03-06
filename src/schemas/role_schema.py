from datetime import datetime

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = None


class RoleResponse(RoleBase):
    id: UUID
    date_created: datetime | None = None
    date_updated: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

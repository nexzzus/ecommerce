"""
Endpoints FastAPI para el recurso de roles.

CRUD de roles y asignación de permisos (PUT /roles/{id}/permissions).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from uuid import UUID

from src.database.config import get_db
from src.entities.roles import Role
from src.entities.permissions import Permission
from src.schemas.role_schema import (
    RoleResponse,
    RoleCreate,
    RoleUpdate,
    RolePermissionsUpdate,
)
from src.core.responses import success_response
from src.core.exceptions import NotFoundError, BadRequestError
from src.core.auth import get_current_user

router = APIRouter(
    prefix="/roles", tags=["roles"], dependecies=[Depends(get_current_user)]
)


@router.get("")
def list_roles(db: Session = Depends(get_db)):
    """
    Lista todos los roles con sus permisos cargados.
    """
    roles = db.query(Role).all()
    data = [RoleResponse.model_validate(r).model_dump(mode="json") for r in roles]
    return success_response(data=data, message="listado de roles")


@router.get("/{role_id}")
def get_role(role_id: UUID, db: Session = Depends(get_db)):
    """
    Devuelve un rol por ID con sus permisos. 404 si no existe.
    """
    role = (
        db.query(Role)
        .options(joinedload(Role.permissions))
        .filter(Role.id == role_id)
        .first()
    )
    if not role:
        raise NotFoundError("Role not found")
    data = RoleResponse.model_validate(role).model_dump(mode="json")
    return success_response(data=data, message="rol obtenido")


@router.post("", status_code=201)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    """
    Crea un rol. 400 si el nombre ya existe.
    """
    if db.query(Role).filter(Role.name == role.name).first():
        raise BadRequestError("el rol ya existe")
    role = Role(name=role.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    data = RoleResponse.model_validate(role).model_dump(mode="json")
    return success_response(data=data, message="rol creado")


@router.put("/{role_id}")
def update_role(role_id: UUID, role: RoleUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un rol por ID. 404 si no existe.
    """
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise NotFoundError("Role not found")
    update = role.model_dump(exclude_unset=True)
    for key, value in update.items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    data = RoleResponse.model_validate(db_role).model_dump(mode="json")
    return success_response(data=data, message="rol actualizado")


@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina un rol por ID. 404 si no existe.
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise NotFoundError("Role not found")
    db.delete(role)
    db.commit()
    return None


@router.put("/{role_id}/permissions")
def set_role_permissions(
    role_id: UUID, body: RolePermissionsUpdate, db: Session = Depends(get_db)
):
    """
    Asigna los permisos a un rol (reemplaza los actuales). N:M.
    404 si el rol no existe. 400 si algún permission_id no existe.
    """
    role = (
        db.query(Role)
        .options(joinedload(Role.permissions))
        .filter(Role.id == role_id)
        .first()
    )
    if not role:
        raise NotFoundError("Role not found")

    perms = db.query(Permission).filter(Permission.id.in_(body.permission_ids)).all()
    if len(perms) != len(body.permission_ids):
        found = {p.id for p in perms}
        missing = set(body.permission_ids) - found
        raise NotFoundError(
            f"Permisos no encontrados: {list(missing)}",
        )
    role.permissions = perms
    db.commit()
    db.refresh(role)
    data = RoleResponse.model_validate(role).model_dump(mode="json")
    return success_response(data=data, message="rol actualizado")

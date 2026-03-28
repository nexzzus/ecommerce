"""
Endpoints FastAPI para el recurso de permisos.

CRUD de permisos (sin relaciones adicionales en los endpoints).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.database.config import get_db
from src.entities.permissions import Permission
from src.schemas.permission_schema import (
    PermissionResponse,
    PermissionCreate,
    PermissionUpdate,
)

from src.core.responses import success_response
from src.core.exceptions import NotFoundError, BadRequestError

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("", response_model=list[PermissionResponse])
def list_permissions(db: Session = Depends(get_db)):
    """
    Lista todos los permisos.
    """
    permissions = db.query(Permission).all()
    data = [
        PermissionResponse.model_validate(p).model_dump(mode="json")
        for p in permissions
    ]
    return success_response(data=data, message="listado de permisos")


@router.get("/{perm_id}", response_model=PermissionResponse)
def get_permission(perm_id: UUID, db: Session = Depends(get_db)):
    """
    Devuelve un permiso por ID. 404 si no existe.
    """
    perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not perm:
        raise NotFoundError(status_code=404, detail="Permission not found")
    data = [PermissionResponse.model_validate(perm).model_dump(mode="json")]
    return success_response(data=data, message="permiso obtenido")


@router.post("", response_model=PermissionResponse, status_code=201)
def create_permission(perm: PermissionCreate, db: Session = Depends(get_db)):
    """
    Crea un permiso. 400 si el nombre ya existe.
    """
    if db.query(Permission).filter(Permission.name == perm.name).first():
        raise BadRequestError(
            message="el permiso ya existe", detail="Permission already registered"
        )
    permission = Permission(
        name=perm.name,
        description=perm.description,
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    data = [PermissionResponse.model_validate(permission).model_dump(mode="json")]
    return success_response(data=data, message="permiso creado")


@router.put("/{perm_id}", response_model=PermissionResponse)
def update_permission(
    perm_id: UUID, permission: PermissionUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza un permiso por ID. 404 si no existe.
    """
    db_perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not db_perm:
        raise NotFoundError("Permission not found")
    update = permission.model_dump(exclude_unset=True)
    for key, value in update.items():
        setattr(db_perm, key, value)
    db.commit()
    db.refresh(db_perm)
    data = [PermissionResponse.model_validate(permission).model_dump(mode="json")]
    return success_response(data=data, message="permiso actualizado")


@router.delete("/{perm_id}", status_code=204)
def delete_permission(perm_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina un permiso por ID. 404 si no existe.
    """
    permission = db.query(Permission).filter(Permission.id == perm_id).first()
    if not permission:
        raise NotFoundError("Permission not found")
    db.delete(permission)
    db.commit()
    return None

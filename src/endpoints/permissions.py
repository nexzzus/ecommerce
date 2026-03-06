from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.database.config import get_db
from src.entities.permissions import Permission
from src.schemas.permission_schema import PermissionResponse, PermissionCreate, PermissionUpdate

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.get("", response_model=list[PermissionResponse])
def list_permissions(db: Session = Depends(get_db)):
    return db.query(Permission).all()

@router.get("/{perm_id}", response_model=PermissionResponse)
def get_role(perm_id: UUID, db: Session = Depends(get_db)):
    perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    return perm

@router.post("", response_model=PermissionResponse, status_code=201)
def create_permission(perm: PermissionCreate, db: Session = Depends(get_db)):
    if db.query(Permission).filter(Permission.name == perm.name).first():
        raise HTTPException(status_code=400, detail="Permission already registered")
    permission = Permission(
        name=perm.name,
        description=perm.description
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

@router.put("/{perm_id}", response_model=PermissionResponse)
def update_permission(perm_id: UUID, permission: PermissionUpdate, db: Session = Depends(get_db)):
    db_perm = db.query(Permission).filter(Permission.id == perm_id).first()
    if not db_perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    update = permission.model_dump(exclude_unset=True)
    for key, value in update.items():
        setattr(db_perm, key, value)
    db.commit()
    db.refresh(db_perm)
    return db_perm

@router.delete("/{perm_id}", status_code=204)
def delete_permission(perm_id: UUID, db: Session = Depends(get_db)):
    permission = db.query(Permission).filter(Permission.id == perm_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(permission)
    db.commit()
    return None
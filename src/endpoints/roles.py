from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.database.config import get_db
from src.entities.roles import Role
from src.entities.users import User
from src.schemas.role_schema import RoleResponse, RoleCreate, RoleUpdate
from src.utils.security import hash_password

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: UUID, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("", response_model=RoleResponse, status_code=201)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    if db.query(Role).filter(Role.name == role.name).first():
        raise HTTPException(status_code=400, detail="Role already registered")
    role = Role(
        name=role.name
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: UUID, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    update = role.model_dump(exclude_unset=True)
    for key, value in update.items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: UUID, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return None
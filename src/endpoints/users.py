from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from uuid import UUID

from src.database.config import get_db
from src.entities.users import User
from src.entities.roles import Role
from src.schemas.user_schema import UserResponse, UserCreate, UserUpdate, UserRolesUpdate
from src.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).options(joinedload(User.roles)).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .options(joinedload(User.roles))
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password),
        phone=user.phone,
        address=user.address
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update = user.model_dump(exclude_unset=True)
    if "password" in update and update["password"]:
        update["password"] = hash_password(update.pop("password"))
    for key, value in update.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None


@router.put("/{user_id}/roles", response_model=UserResponse)
def set_user_roles(user_id: UUID, body: UserRolesUpdate, db: Session = Depends(get_db)):
    """Asigna los roles a un usuario (reemplaza los actuales). N:M."""
    user = (
        db.query(User)
        .options(joinedload(User.roles))
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    roles = db.query(Role).filter(Role.id.in_(body.role_ids)).all()
    if len(roles) != len(body.role_ids):
        found = {r.id for r in roles}
        missing = set(body.role_ids) - found
        raise HTTPException(
            status_code=400,
            detail=f"Roles no encontrados: {list(missing)}",
        )
    user.roles = roles
    db.commit()
    db.refresh(user)
    return user
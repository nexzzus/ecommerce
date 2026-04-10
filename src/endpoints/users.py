"""
Endpoints FastAPI para el recurso de usuarios.

CRUD de usuarios y asignación de roles (PUT /users/{id}/roles).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from uuid import UUID

from src.database.config import get_db
from src.entities.users import User
from src.entities.roles import Role
from src.schemas.user_schema import (
    UserResponse,
    UserCreate,
    UserUpdate,
    UserRolesUpdate,
)
from src.utils.security import hash_password
from src.core.responses import success_response
from src.core.exceptions import NotFoundError, BadRequestError
from src.core.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", dependecies=[Depends(get_current_user)])
def list_users(db: Session = Depends(get_db)):
    """
    Lista todos los usuarios con sus roles cargados.
    """
    users = db.query(User).all()
    data = [UserResponse.model_validate(u).model_dump(mode="json") for u in users]
    return success_response(data=data, message="listado de usuarios")


@router.get("/{user_id}", dependecies=[Depends(get_current_user)])
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Devuelve un usuario por ID con sus roles. 404 si no existe.
    """
    user = (
        db.query(User)
        .options(joinedload(User.roles))
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise NotFoundError("User not found")
    data = UserResponse.model_validate(user).model_dump(mode="json")
    return success_response(data=data, message="usuario obtenido")


@router.post("", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un usuario. La contraseña se hashea. Opcionalmente se pueden
    asignar roles (role_ids). 400 si el email ya existe o si algún role_id
    no existe.
    """
    if db.query(User).filter(User.email == user.email).first():
        raise BadRequestError("Email already registered")
    roles_to_assign = None
    if user.role_ids:
        roles_to_assign = db.query(Role).filter(Role.id.in_(user.role_ids)).all()
        if len(roles_to_assign) != len(user.role_ids):
            found = {r.id for r in roles_to_assign}
            missing = set(user.role_ids) - found
            raise NotFoundError(
                f"Roles no encontrados: {list(missing)}",
            )
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password),
        phone=user.phone,
        address=user.address,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if roles_to_assign:
        db_user.roles = roles_to_assign
        db.commit()
        db.refresh(db_user)
    data = UserResponse.model_validate(db_user).model_dump(mode="json")
    return success_response(data=data, message="usuario creado")


@router.put("/{user_id}", dependecies=[Depends(get_current_user)])
def update_user(user_id: UUID, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un usuario por ID (solo campos enviados). 404 si no existe.
    Si se envía password, se hashea antes de guardar.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise NotFoundError("User not found")
    update = user.model_dump(exclude_unset=True)
    if "password" in update and update["password"]:
        update["password"] = hash_password(update.pop("password"))
    for key, value in update.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    data = UserResponse.model_validate(db_user).model_dump(mode="json")
    return success_response(data=data, message="usuario actualizado")


@router.delete("/{user_id}", status_code=204, dependecies=[Depends(get_current_user)])
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina un usuario por ID. 404 si no existe.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError("User not found")
    db.delete(user)
    db.commit()
    return None


@router.put("/{user_id}/roles", dependecies=[Depends(get_current_user)])
def set_user_roles(user_id: UUID, body: UserRolesUpdate, db: Session = Depends(get_db)):
    """
    Asigna los roles a un usuario (reemplaza los actuales). N:M.
    404 si el usuario no existe. 400 si algún role_id no existe.
    """
    user = (
        db.query(User)
        .options(joinedload(User.roles))
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise NotFoundError("User not found")
    roles = db.query(Role).filter(Role.id.in_(body.role_ids)).all()
    if len(roles) != len(body.role_ids):
        found = {r.id for r in roles}
        missing = set(body.role_ids) - found
        raise NotFoundError(
            f"Roles no encontrados: {list(missing)}",
        )
    user.roles = roles
    db.commit()
    db.refresh(user)
    data = UserResponse.model_validate(user).model_dump(mode="json")
    return success_response(data=data, message="usuario actualizado")

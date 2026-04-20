from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.core.auth import create_access_token
from src.core.security import verify_password
from src.database.database import get_db
from src.entities.users import User
from src.core.config import get_settings

router = APIRouter()

settings = get_settings()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autenticación de usuario para obtener un access token.
    Compatible con flujos de seguridad OAuth2.
    """

    # 1. Búsqueda del usuario por el email ingresado en el formulario
    user = db.query(User).filter(User.email == form_data.username).first()

    # 2. Validar existencia y contraseña (en una sola validación)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Generación del JWT Token real usando el email del usuario
    access_token = create_access_token(
        subject = user.id,
        nombre_usuario=f"{user.first_name} {user.last_name}",
        rol=user.roles[0].name if user.roles else "USER",
        settings=settings
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

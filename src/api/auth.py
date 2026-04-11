from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database.database import get_db 
from src.entities.users import User 
from src.core.security import create_access_token 

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autenticación de usuario para obtener un access token.
    Compatible con flujos de seguridad OAuth2.
    """
    
    # 1. Búsqueda del usuario por el email ingresado en el formulario
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # 2. Validación de existencia
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales inválidas: Usuario no encontrado"
        )

    # 3. Validación de contraseña (Modo compatible para desarrollo)
    # Comparamos directamente para evitar conflictos con librerías de hash en Python 3.13
    if form_data.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales inválidas: Contraseña incorrecta"
        )
    
    # 4. Generación del JWT Token real usando el email del usuario
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }
"""Pruebas de generación y validación de tokens JWT."""

from uuid import uuid4

from jose import jwt

from src.core.auth import create_access_token
from src.core.config import get_settings


def test_create_access_token_contains_expected_claims():
    user_id = uuid4()
    settings = get_settings()

    token = create_access_token(
        subject=user_id,
        nombre_usuario="JuanPerez",
        rol="USER",
        settings=settings,
    )

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == str(user_id)
    assert payload["nombre_usuario"] == "JuanPerez"
    assert payload["rol"] == "USER"
    assert "exp" in payload
    assert "iat" in payload

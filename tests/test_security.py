"""Pruebas de utilidades de seguridad (hashing de contraseñas)."""

import bcrypt

from src.utils.security import hash_password


def test_hash_password_returns_bcrypt_hash():
    hashed = hash_password("mi-clave-segura")

    assert hashed.startswith("$2b$")
    assert bcrypt.checkpw(b"mi-clave-segura", hashed.encode("utf-8"))


def test_hash_password_uses_different_salts():
    hash_a = hash_password("misma-clave")
    hash_b = hash_password("misma-clave")

    assert hash_a != hash_b
    assert bcrypt.checkpw(b"misma-clave", hash_a.encode("utf-8"))
    assert bcrypt.checkpw(b"misma-clave", hash_b.encode("utf-8"))

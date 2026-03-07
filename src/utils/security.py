"""
Utilidades de seguridad: hashing de contraseñas con bcrypt.
"""
import bcrypt


def hash_password(plain: str) -> str:
    """
    Hashea una contraseña en texto plano con bcrypt.

    Args:
        plain: Contraseña en texto plano.

    Returns:
        Contraseña hasheada como string (utf-8).
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain.encode("utf-8"), salt)
    return hashed.decode("utf-8")

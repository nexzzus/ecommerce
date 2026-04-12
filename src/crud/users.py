"""
Cliente CRUD para el recurso de usuarios de la API.

Expone list_users, get_user, create_user, update_user, delete_user
y set_user_roles. Todas las funciones delegan en el cliente HTTP (client.py).
"""

from src.crud.client import _get, _post, _put, _delete


def list_users() -> list:
    """
    Obtiene la lista de todos los usuarios (incluye roles).

    Returns:
        Lista de diccionarios con los datos de cada usuario.
    """
    return _get("/users")


def get_user(user_id: str) -> dict:
    """
    Obtiene un usuario por ID.

    Args:
        user_id: UUID del usuario.

    Returns:
        Diccionario con los datos del usuario y su lista de roles.
    """
    return _get(f"/users/{user_id}")


def create_user(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    phone: str | None = None,
    address: str | None = None,
    role_ids: list | None = None,
) -> dict:
    """
    Crea un nuevo usuario. Opcionalmente asigna roles (role_ids).

    Args:
        first_name: Nombre.
        last_name: Apellido.
        email: Email (válido).
        password: Contraseña en texto plano (se hashea en el servidor).
        phone: Teléfono opcional.
        address: Dirección opcional.
        role_ids: Lista de UUIDs de roles a asignar (opcional).

    Returns:
        Usuario creado tal como lo devuelve la API.
    """
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone": phone,
        "address": address,
    }
    if role_ids is not None:
        payload["role_ids"] = role_ids
    return _post("/users", json=payload)


def register_user(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    phone: str | None = None,
    address: str | None = None,
) -> dict:
    """
    Registra un nuevo usuario..

    Args:
        first_name: Nombre.
        last_name: Apellido.
        email: Email (válido).
        password: Contraseña en texto plano (se hashea en el servidor).
        phone: Teléfono opcional.
        address: Dirección opcional.
    Returns:
        Usuario creado tal como lo devuelve la API.
    """
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone": phone,
        "address": address,
    }
    return _post("/users/register", json=payload)


def update_user(
    user_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    password: str | None = None,
    phone: str | None = None,
    address: str | None = None,
) -> dict:
    """
    Actualiza un usuario existente (solo los campos no None).

    Args:
        user_id: UUID del usuario.
        first_name: Nuevo nombre (opcional).
        last_name: Nuevo apellido (opcional).
        email: Nuevo email (opcional).
        password: Nueva contraseña (opcional).
        phone: Nuevo teléfono (opcional).
        address: Nueva dirección (opcional).

    Returns:
        Usuario actualizado.
    """
    payload = {}
    if first_name is not None:
        payload["first_name"] = first_name
    if last_name is not None:
        payload["last_name"] = last_name
    if email is not None:
        payload["email"] = email
    if password is not None:
        payload["password"] = password
    if phone is not None:
        payload["phone"] = phone
    if address is not None:
        payload["address"] = address
    return _put(f"/users/{user_id}", json=payload)


def delete_user(user_id: str) -> None:
    """
    Elimina un usuario por ID.

    Args:
        user_id: UUID del usuario.
    """
    _delete(f"/users/{user_id}")


def set_user_roles(user_id: str, role_ids: list) -> dict:
    """
    Asigna los roles a un usuario (reemplaza los actuales). Relación N:M.

    Args:
        user_id: UUID del usuario.
        role_ids: Lista de UUIDs de roles.

    Returns:
        Usuario actualizado con la nueva lista de roles.
    """
    return _put(f"/users/{user_id}/roles", json={"role_ids": role_ids})

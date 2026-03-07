"""
Cliente CRUD para el recurso de roles de la API.

Expone list_roles, get_role, create_role, update_role, delete_role
y set_role_permissions.
"""
from src.crud.client import _get, _post, _put, _delete


def list_roles() -> list:
    """
    Obtiene la lista de todos los roles (incluye permisos).

    Returns:
        Lista de diccionarios con los datos de cada rol.
    """
    return _get("/roles")


def get_role(role_id: str) -> dict:
    """
    Obtiene un rol por ID.

    Args:
        role_id: UUID del rol.

    Returns:
        Diccionario con los datos del rol y su lista de permisos.
    """
    return _get(f"/roles/{role_id}")


def create_role(name: str) -> dict:
    """
    Crea un nuevo rol.

    Args:
        name: Nombre del rol.

    Returns:
        Rol creado tal como lo devuelve la API.
    """
    payload = {"name": name}
    return _post("/roles", json=payload)


def update_role(role_id: str, name: str | None = None) -> dict:
    """
    Actualiza un rol existente.

    Args:
        role_id: UUID del rol.
        name: Nuevo nombre (opcional).

    Returns:
        Rol actualizado.
    """
    payload = {}
    if name is not None:
        payload["name"] = name
    return _put(f"/roles/{role_id}", json=payload)


def delete_role(role_id: str) -> None:
    """
    Elimina un rol por ID.

    Args:
        role_id: UUID del rol.
    """
    _delete(f"/roles/{role_id}")


def set_role_permissions(role_id: str, permission_ids: list) -> dict:
    """
    Asigna los permisos a un rol (reemplaza los actuales). Relación N:M.

    Args:
        role_id: UUID del rol.
        permission_ids: Lista de UUIDs de permisos.

    Returns:
        Rol actualizado con la nueva lista de permisos.
    """
    return _put(
        f"/roles/{role_id}/permissions",
        json={"permission_ids": permission_ids},
    )

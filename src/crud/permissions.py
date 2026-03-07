"""
Cliente CRUD para el recurso de permisos de la API.

Expone list_permissions, get_permission, create_permission,
update_permission y delete_permission.
"""
from src.crud.client import _get, _post, _put, _delete


def list_permissions() -> list:
    """
    Obtiene la lista de todos los permisos.

    Returns:
        Lista de diccionarios con los datos de cada permiso.
    """
    return _get("/permissions")


def get_permission(perm_id: str) -> dict:
    """
    Obtiene un permiso por ID.

    Args:
        perm_id: UUID del permiso.

    Returns:
        Diccionario con los datos del permiso.
    """
    return _get(f"/permissions/{perm_id}")


def create_permission(name: str, description: str | None = None) -> dict:
    """
    Crea un nuevo permiso.

    Args:
        name: Nombre del permiso.
        description: Descripción opcional.

    Returns:
        Permiso creado tal como lo devuelve la API.
    """
    payload = {"name": name, "description": description}
    return _post("/permissions", json=payload)


def update_permission(
    permission_id: str,
    name: str | None = None,
    description: str | None = None,
) -> dict:
    """
    Actualiza un permiso existente.

    Args:
        permission_id: UUID del permiso.
        name: Nuevo nombre (opcional).
        description: Nueva descripción (opcional).

    Returns:
        Permiso actualizado.
    """
    payload = {}
    if name is not None:
        payload["name"] = name
    if description is not None:
        payload["description"] = description
    return _put(f"/permissions/{permission_id}", json=payload)


def delete_permission(perm_id: str) -> None:
    """
    Elimina un permiso por ID.

    Args:
        perm_id: UUID del permiso.
    """
    _delete(f"/permissions/{perm_id}")

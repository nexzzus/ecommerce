from src.crud.client import _get, _post, _put, _delete


def list_roles() -> list:
    return _get("/roles")


def get_role(role_id: str) -> dict:
    return _get(f"/roles/{role_id}")


def create_role(
        name: str
) -> dict:
    payload = {
        "name": name,
    }
    return _post("/roles", json=payload)


def update_role(
        role_id: str,
        name: str | None = None,
) -> dict:
    payload = {}
    if name is not None:
        payload["name"] = name

    return _put(f"/roles/{role_id}", json=payload)

def delete_role(role_id: str) -> None:
    _delete(f"/roles/{role_id}")


def set_role_permissions(role_id: str, permission_ids: list) -> dict:
    """Asigna los permisos a un rol (reemplaza los actuales)."""
    return _put(f"/roles/{role_id}/permissions", json={"permission_ids": permission_ids})
from src.crud.client import _get, _post, _put, _delete


def list_permissions() -> list:
    return _get("/permissions")


def get_permission(perm_id: str) -> dict:
    return _get(f"/permissions/{perm_id}")


def create_permission(
        name: str,
        description: str | None = None
) -> dict:
    payload = {
        "name": name,
        "description": description
    }
    return _post("/permissions", json=payload)


def update_permission(
        permission_id: str,
        name: str | None = None,
        description: str | None = None
) -> dict:
    payload = {}
    if name is not None:
        payload["name"] = name
    if description is not None:
        payload["description"] = description
    return _put(f"/permissions/{permission_id}", json=payload)


def delete_permission(perm_id: str) -> None:
    _delete(f"/permissions/{perm_id}")

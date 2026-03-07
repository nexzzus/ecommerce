from src.crud.client import _get, _post, _put, _delete


def list_users() -> list:
    return _get("/users")


def get_user(user_id: str) -> dict:
    return _get(f"/users/{user_id}")


def create_user(
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        phone: str | None = None,
        address: str | None = None
) -> dict:
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone": phone,
        "address": address
    }
    return _post("/users", json=payload)


def update_user(
        user_id: str,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        password: str | None = None,
        phone: str | None = None,
        address: str | None = None
) -> dict:
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
    _delete(f"/users/{user_id}")


def set_user_roles(user_id: str, role_ids: list) -> dict:
    """Asigna los roles a un usuario (reemplaza los actuales)."""
    return _put(f"/users/{user_id}/roles", json={"role_ids": role_ids})
"""

Cliente CRUD para líneas del carrito contra la API HTTP.

"""

from src.crud.client import _delete, _get, _post, _put


def list_cart_items() -> list:
    """Lista todas las líneas del carrito."""
    return _get("/cart-items")


def get_cart_item(cart_item_id: str) -> dict:
    """Obtiene una línea por ID (incluye user y product anidados)."""
    return _get(f"/cart-items/{cart_item_id}")


def create_cart_item(
    id_product: str,
    quantity: int,
    id_user: str | None = None,
) -> dict:
    """Crea una línea de carrito."""
    payload: dict = {"id_product": id_product, "quantity": quantity}
    if id_user is not None:
        payload["id_user"] = id_user
    return _post("/cart-items", json=payload)


def update_cart_item(
    cart_item_id: str,
    quantity: int | None = None,
    id_user: str | None = None,
    clear_user: bool = False,
) -> dict:
    """
    Actualiza una línea. Si clear_user es True, envía id_user null en el body.
    """
    payload: dict = {}
    if quantity is not None:
        payload["quantity"] = quantity
    if clear_user:
        payload["id_user"] = None
    elif id_user is not None:
        payload["id_user"] = id_user
    return _put(f"/cart-items/{cart_item_id}", json=payload)


def delete_cart_item(cart_item_id: str) -> None:
    """Elimina una línea del carrito."""
    _delete(f"/cart-items/{cart_item_id}")

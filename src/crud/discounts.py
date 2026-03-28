"""

Cliente CRUD para el recurso de descuentos de la API.

Expone list_discounts, get_discount, create_discount, update_discount, delete_discount.

"""

from src.crud.client import _get, _post, _put, _delete


def list_discounts() -> list:
    """

    Obtiene la lista de todos los descuentos.

    Returns:

        Lista de diccionarios con los datos de cada descuento.

    """

    return _get("/discounts")


def get_discount(discount_id: str) -> dict:
    """

    Obtiene un descuento por ID.

    Args:

        discount_id: UUID del descuento.

    Returns:

        Diccionario con los datos del descuento.

    """

    return _get(f"/discounts/{discount_id}")


def create_discount(value: float | str, code: str, status: str = "active") -> dict:
    """

    Crea un nuevo descuento.

    Args:

        value: Valor del descuento (porcentaje o monto).

        code: Código único del descuento.

        status: Estado (por defecto "active").

    Returns:

        Descuento creado tal como lo devuelve la API.

    """

    payload = {"value": str(value), "code": code, "status": status}

    return _post("/discounts", json=payload)


def update_discount(
    discount_id: str,
    value: float | str | None = None,
    code: str | None = None,
    status: str | None = None,
) -> dict:
    """

    Actualiza un descuento existente.

    Args:

        discount_id: UUID del descuento.

        value: Nuevo valor (opcional).

        code: Nuevo código (opcional).

        status: Nuevo estado (opcional).

    Returns:

        Descuento actualizado.

    """

    payload = {}

    if value is not None:
        payload["value"] = str(value)

    if code is not None:
        payload["code"] = code

    if status is not None:
        payload["status"] = status

    return _put(f"/discounts/{discount_id}", json=payload)


def delete_discount(discount_id: str) -> None:
    """

    Elimina un descuento por ID.

    Args:

        discount_id: UUID del descuento.

    """

    _delete(f"/discounts/{discount_id}")

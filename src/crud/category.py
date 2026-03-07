"""

Cliente CRUD para el recurso de categorías de la API.

Expone list_categories, get_category, create_category, update_category, delete_category.

"""

from src.crud.client import _get, _post, _put, _delete


def list_categories() -> list:
    """

    Obtiene la lista de todas las categorías.

    Returns:

        Lista de diccionarios con los datos de cada categoría.

    """

    return _get("/categories")


def get_category(category_id: str) -> dict:
    """

    Obtiene una categoría por ID.

    Args:

        category_id: UUID de la categoría.

    Returns:

        Diccionario con los datos de la categoría.

    """

    return _get(f"/categories/{category_id}")


def create_category(name: str) -> dict:
    """

    Crea una nueva categoría.

    Args:

        name: Nombre de la categoría.

    Returns:

        Categoría creada tal como lo devuelve la API.

    """

    payload = {"name": name}

    return _post("/categories", json=payload)


def update_category(category_id: str, name: str | None = None) -> dict:
    """

    Actualiza una categoría existente.

    Args:

        category_id: UUID de la categoría.

        name: Nuevo nombre (opcional).

    Returns:

        Categoría actualizada.

    """

    payload = {}

    if name is not None:

        payload["name"] = name

    return _put(f"/categories/{category_id}", json=payload)


def delete_category(category_id: str) -> None:
    """

    Elimina una categoría por ID.

    Args:

        category_id: UUID de la categoría.

    """

    _delete(f"/categories/{category_id}")

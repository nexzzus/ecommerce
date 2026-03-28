"""

Cliente CRUD para el recurso de productos de la API.

Expone list_products, get_product, create_product, update_product, delete_product

y set_product_categories.

"""

from src.crud.client import _get, _post, _put, _delete


def list_products() -> list:
    """

    Obtiene la lista de todos los productos (incluye descuento y categorías).

    Returns:

        Lista de diccionarios con los datos de cada producto.

    """

    return _get("/products")


def get_product(product_id: str) -> dict:
    """

    Obtiene un producto por ID.

    Args:

        product_id: UUID del producto.

    Returns:

        Diccionario con los datos del producto, descuento y categorías.

    """

    return _get(f"/products/{product_id}")


def create_product(
    name: str,
    price: float | str,
    description: str | None = None,
    stock: int = 0,
    id_discount: str | None = None,
    category_ids: list | None = None,
) -> dict:
    """

    Crea un nuevo producto.

    Args:

        name: Nombre del producto.

        price: Precio.

        description: Descripción (opcional).

        stock: Stock (por defecto 0).

        id_discount: UUID del descuento (opcional).

        category_ids: Lista de UUIDs de categorías (opcional).

    Returns:

        Producto creado tal como lo devuelve la API.

    """

    payload = {
        "name": name,
        "price": str(price),
        "description": description,
        "stock": stock,
    }

    if id_discount is not None:
        payload["id_discount"] = id_discount

    if category_ids is not None:
        payload["category_ids"] = category_ids

    return _post("/products", json=payload)


def update_product(
    product_id: str,
    name: str | None = None,
    price: float | str | None = None,
    description: str | None = None,
    stock: int | None = None,
    id_discount: str | None = None,
) -> dict:
    """

    Actualiza un producto existente.

    Args:

        product_id: UUID del producto.

        name: Nuevo nombre (opcional).

        price: Nuevo precio (opcional).

        description: Nueva descripción (opcional).

        stock: Nuevo stock (opcional).

        id_discount: UUID del descuento o None (opcional).

    Returns:

        Producto actualizado.

    """

    payload = {}

    if name is not None:
        payload["name"] = name

    if price is not None:
        payload["price"] = str(price)

    if description is not None:
        payload["description"] = description

    if stock is not None:
        payload["stock"] = stock

    if id_discount is not None:
        payload["id_discount"] = id_discount

    return _put(f"/products/{product_id}", json=payload)


def delete_product(product_id: str) -> None:
    """

    Elimina un producto por ID.

    Args:

        product_id: UUID del producto.

    """

    _delete(f"/products/{product_id}")


def set_product_categories(product_id: str, category_ids: list) -> dict:
    """

    Asigna las categorías a un producto (reemplaza las actuales). N:M.

    Args:

        product_id: UUID del producto.

        category_ids: Lista de UUIDs de categorías.

    Returns:

        Producto actualizado con la nueva lista de categorías.

    """

    return _put(
        f"/products/{product_id}/categories",
        json={"category_ids": category_ids},
    )

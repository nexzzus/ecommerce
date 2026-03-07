from src.crud.client import _get, _post, _put, _delete


def list_products() -> list:
    """
    Obtiene la lista de todos los productos.

    Returns:
        Lista de diccionarios con los datos de cada producto
    """
    return _get("/products")


def get_product(product_id: str) -> dict:
    """
    Obtiene un product por ID.

    Args:
        product_id: UUID del product.

    Returns:
        Diccionario con los datos del product
    """
    return _get(f"/products/{product_id}")


def create_product(name: str, price: float, description: str, stock: int) -> dict:
    """
    Crea un nuevo product

    Args:
        name: Nombre
        price: Precio
        description: Descripcion
        stock: Cantidad

    Returns:
        Producto creado tal como lo devuelve la API.
    """
    payload = {"name": name, "price": price, "description": description, "stock": stock}

    return _post("/products", json=payload)


def update_product(
    product_id: str,
    name: str,
    price: float,
    description: str,
    stock: int,
) -> dict:
    """
    Actualiza un producto

    Args:
        user_product: UUID del producto.
        name: Nuevo nombre del producto,
        price: Nuevo precio del producto.
        description: Nueva descripcion del producto.
        stock: Nueva cantidad del producto.


    Returns:
        Producto actualizado.
    """
    payload = {}
    if name is not None:
        payload["name"] = name
    if price is not None:
        payload["price"] = price
    if description is not None:
        payload["description"] = description
    if stock is not None:
        payload["stock"] = stock
    return _put(f"/products/{product_id}", json=payload)


def delete_product(product_id: str) -> None:
    """
    Elimina un producto por ID.

    Args:
        product_id: UUID del Producto.
    """
    _delete(f"/products/{product_id}")

"""
Endpoints FastAPI para líneas del carrito (cart_items).

CRUD con validación de existencia de usuario (si se envía) y producto.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from src.schemas.product_schema import ProductResponse
from src.database.config import get_db
from src.entities.cart_items import CartItem
from src.entities.products import Product
from src.entities.users import User
from src.schemas.cart_item_schema import (
    CartItemCreate,
    CartItemDetailResponse,
    CartItemResponse,
    CartItemUpdate,
)
from src.core.responses import success_response
from src.core.exceptions import NotFoundError

router = APIRouter(prefix="/cart-items", tags=["cart-items"])


def _load_cart_item_detail(query):
    """Eager load user (roles), product (discount, categories) para respuestas detalladas."""
    return query.options(
        joinedload(CartItem.user).joinedload(User.roles),
        joinedload(CartItem.product).joinedload(Product.discount),
        joinedload(CartItem.product).joinedload(Product.categories),
    )


@router.get("")
def list_cart_items(db: Session = Depends(get_db)):
    """Lista todas las líneas del carrito."""
    items = db.query(CartItem).all()
    data = [
        CartItemResponse.model_validate(item).model_dump(mode="json") for item in items
    ]
    return success_response(data=data, message="listado de articulos")


@router.get("/{cart_item_id}")
def get_cart_item(cart_item_id: UUID, db: Session = Depends(get_db)):
    """Obtiene una línea por ID con usuario y producto relacionados."""
    item = (
        _load_cart_item_detail(db.query(CartItem))
        .filter(CartItem.id == cart_item_id)
        .first()
    )
    if not item:
        raise NotFoundError("Cart item not found")
    data = ProductResponse.model_validate(item).model_dump(mode="json")
    return success_response(data=data, message="cart item obtenido")


@router.post("", status_code=201)
def create_cart_item(body: CartItemCreate, db: Session = Depends(get_db)):
    """Crea una línea. Verifica que el producto (y el usuario si aplica) existan."""
    if body.id_user is not None:
        user = db.query(User).filter(User.id == body.id_user).first()
        if not user:
            raise NotFoundError("Usuario no encontrado")
    product = db.query(Product).filter(Product.id == body.id_product).first()
    if not product:
        raise NotFoundError("Producto no encontrado")
    db_item = CartItem(
        id_user=body.id_user,
        id_product=body.id_product,
        quantity=body.quantity,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    item = (
        _load_cart_item_detail(db.query(CartItem))
        .filter(CartItem.id == db_item.id)
        .first()
    )
    data = CartItemResponse.model_validate(item).model_dump(mode="json")
    return success_response(data=data, message="cart item creado")


@router.put("/{cart_item_id}")
def update_cart_item(
    cart_item_id: UUID, body: CartItemUpdate, db: Session = Depends(get_db)
):
    """Actualiza cantidad y/o usuario. 404 si la línea no existe."""
    item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not item:
        raise NotFoundError("Cart item not found")
    data = body.model_dump(exclude_unset=True)
    if not data:
        raise NotFoundError("No hay campos para actualizar")
    if "id_user" in data and data["id_user"] is not None:
        user = db.query(User).filter(User.id == data["id_user"]).first()
        if not user:
            raise NotFoundError("Usuario no encontrado")
    for key, value in data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    updated = (
        _load_cart_item_detail(db.query(CartItem))
        .filter(CartItem.id == cart_item_id)
        .first()
    )
    data = CartItemResponse.model_validate(updated).model_dump(mode="json")
    return success_response(data=data, message="cart item actualizado")


@router.delete("/{cart_item_id}", status_code=204)
def delete_cart_item(cart_item_id: UUID, db: Session = Depends(get_db)):
    """Elimina una línea del carrito."""
    item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not item:
        raise NotFoundError("Cart item not found")
    db.delete(item)
    db.commit()
    return None

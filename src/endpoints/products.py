"""

Endpoints FastAPI para el recurso de productos.

CRUD de productos y asignación de categorías (PUT /products/{id}/categories).

"""

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session, joinedload

from uuid import UUID

from src.database.config import get_db

from src.entities.products import Product

from src.entities.discounts import Discount

from src.entities.category import Category

from src.schemas.product_schema import (
    ProductResponse,
    ProductCreate,
    ProductUpdate,
    ProductCategoriesUpdate,
)

router = APIRouter(prefix="/products", tags=["products"])


def _load_product_relations(query):
    """Carga producto con discount y categories."""

    return query.options(
        joinedload(Product.discount),
        joinedload(Product.categories),
    )


@router.get("", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    """

    Lista todos los productos con descuento y categorías.

    """

    return _load_product_relations(db.query(Product)).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    """

    Devuelve un producto por ID con descuento y categorías. 404 si no existe.

    """

    product = (
        _load_product_relations(db.query(Product))
        .filter(Product.id == product_id)
        .first()
    )

    if not product:

        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """

    Crea un producto. Opcionalmente id_discount y category_ids.

    400 si id_discount no existe o algún category_id no existe.

    """

    discount = None

    if product.id_discount:

        discount = db.query(Discount).filter(Discount.id == product.id_discount).first()

        if not discount:

            raise HTTPException(status_code=400, detail="Discount not found")

    categories_to_assign = []

    if product.category_ids:

        categories_to_assign = (
            db.query(Category).filter(Category.id.in_(product.category_ids)).all()
        )

        if len(categories_to_assign) != len(product.category_ids):

            found = {c.id for c in categories_to_assign}

            missing = set(product.category_ids) - found

            raise HTTPException(
                status_code=400,
                detail=f"Categorías no encontradas: {list(missing)}",
            )

    db_product = Product(
        id_discount=product.id_discount,
        name=product.name,
        price=product.price,
        description=product.description,
        stock=product.stock,
    )

    db.add(db_product)

    db.commit()

    db.refresh(db_product)

    if categories_to_assign:

        db_product.categories = categories_to_assign

        db.commit()

        db.refresh(db_product)

    return _load_product_relations(
        db.query(Product).filter(Product.id == db_product.id)
    ).first()


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: UUID, product: ProductUpdate, db: Session = Depends(get_db)
):
    """

    Actualiza un producto por ID (solo campos enviados). 404 si no existe.

    400 si se envía id_discount que no existe.

    """

    db_product = (
        _load_product_relations(db.query(Product))
        .filter(Product.id == product_id)
        .first()
    )

    if not db_product:

        raise HTTPException(status_code=404, detail="Product not found")

    update = product.model_dump(exclude_unset=True)

    if "id_discount" in update and update["id_discount"] is not None:

        discount = (
            db.query(Discount).filter(Discount.id == update["id_discount"]).first()
        )

        if not discount:

            raise HTTPException(status_code=400, detail="Discount not found")

    for key, value in update.items():

        setattr(db_product, key, value)

    db.commit()

    db.refresh(db_product)

    return _load_product_relations(
        db.query(Product).filter(Product.id == product_id)
    ).first()


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    """

    Elimina un producto por ID. 404 si no existe.

    """

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:

        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)

    db.commit()

    return None


@router.put("/{product_id}/categories", response_model=ProductResponse)
def set_product_categories(
    product_id: UUID, body: ProductCategoriesUpdate, db: Session = Depends(get_db)
):
    """

    Asigna las categorías a un producto (reemplaza las actuales). N:M.

    404 si el producto no existe. 400 si algún category_id no existe.

    """

    product = (
        _load_product_relations(db.query(Product))
        .filter(Product.id == product_id)
        .first()
    )

    if not product:

        raise HTTPException(status_code=404, detail="Product not found")

    categories = db.query(Category).filter(Category.id.in_(body.category_ids)).all()

    if len(categories) != len(body.category_ids):

        found = {c.id for c in categories}

        missing = set(body.category_ids) - found

        raise HTTPException(
            status_code=400,
            detail=f"Categorías no encontradas: {list(missing)}",
        )

    product.categories = categories

    db.commit()

    db.refresh(product)

    return product

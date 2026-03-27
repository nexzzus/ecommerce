"""

Endpoints FastAPI para el recurso de categorías.

CRUD de categorías.

"""

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from uuid import UUID

from src.database.config import get_db

from src.entities.category import Category

from src.schemas.category_schema import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
)
from src.core.responses import success_response
from src.core.exceptions import NotFoundError, BadRequestError

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """

    Lista todas las categorías.

    """
    categorys = db.query(Category).all()
    data = [
        CategoryResponse.model_validate(c).model_dump(mode="json") for c in categorys
    ]
    return success_response(data=data, message="listado de categorias")


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    """

    Devuelve una categoría por ID. 404 si no existe.

    """

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:

        raise NotFoundError("Category not found")

    data = [CategoryResponse.model_validate(category).model_dump(mode="json")]
    return success_response(data=data, message="categoria obtenida")


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """

    Crea una categoría. 400 si el nombre ya existe.

    """

    if db.query(Category).filter(Category.name == category.name).first():

        raise BadRequestError(
            message="categoria ya existente", detail="Category name already registered"
        )

    db_category = Category(name=category.name)

    db.add(db_category)

    db.commit()

    db.refresh(db_category)

    data = [CategoryResponse.model_validate(db_category).model_dump(mode="json")]
    return success_response(data=data, message="categoria creada")


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: UUID, category: CategoryUpdate, db: Session = Depends(get_db)
):
    """

    Actualiza una categoría por ID. 404 si no existe.

    """

    db_category = db.query(Category).filter(Category.id == category_id).first()

    if not db_category:

        raise NotFoundError("Category not found")

    update = category.model_dump(exclude_unset=True)

    for key, value in update.items():

        setattr(db_category, key, value)

    db.commit()

    db.refresh(db_category)

    data = [CategoryResponse.model_validate(db_category).model_dump(mode="json")]
    return success_response(data=data, message="categoria actualizada")


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    """

    Elimina una categoría por ID. 404 si no existe.

    """

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:

        raise NotFoundError("Category not found")

    db.delete(category)

    db.commit()

    return None

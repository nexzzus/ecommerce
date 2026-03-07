"""
Endpoints FastAPI para el recurso de descuentos.

CRUD de descuentos.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.database.config import get_db
from src.entities.discounts import Discount
from src.schemas.discount_schema import (
    DiscountResponse,
    DiscountCreate,
    DiscountUpdate,
)

router = APIRouter(prefix="/discounts", tags=["discounts"])


@router.get("", response_model=list[DiscountResponse])
def list_discounts(db: Session = Depends(get_db)):
    """
    Lista todos los descuentos.
    """
    return db.query(Discount).all()


@router.get("/{discount_id}", response_model=DiscountResponse)
def get_discount(discount_id: UUID, db: Session = Depends(get_db)):
    """
    Devuelve un descuento por ID. 404 si no existe.
    """
    discount = db.query(Discount).filter(Discount.id == discount_id).first()
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount


@router.post("", response_model=DiscountResponse, status_code=201)
def create_discount(discount: DiscountCreate, db: Session = Depends(get_db)):
    """
    Crea un descuento. 400 si el código ya existe.
    """
    if db.query(Discount).filter(Discount.code == discount.code).first():
        raise HTTPException(status_code=400, detail="Discount code already registered")
    db_discount = Discount(
        value=discount.value,
        code=discount.code,
        status=discount.status,
    )
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)
    return db_discount


@router.put("/{discount_id}", response_model=DiscountResponse)
def update_discount(
    discount_id: UUID, discount: DiscountUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza un descuento por ID. 404 si no existe.
    """
    db_discount = db.query(Discount).filter(Discount.id == discount_id).first()
    if not db_discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    update = discount.model_dump(exclude_unset=True)
    for key, value in update.items():
        setattr(db_discount, key, value)
    db.commit()
    db.refresh(db_discount)
    return db_discount


@router.delete("/{discount_id}", status_code=204)
def delete_discount(discount_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina un descuento por ID. 404 si no existe.
    """
    discount = db.query(Discount).filter(Discount.id == discount_id).first()
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    db.delete(discount)
    db.commit()
    return None

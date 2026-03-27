from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.crud import orden_crud

from src.database.database import SessionLocal
from src.schemas.orden_schema import OrdenCreate
from src.crud.orden_crud import (
    crear_orden,
    obtener_orden,
    obtener_ordenes,
    eliminar_orden,
)

router = APIRouter(prefix="/orden", tags=["Orden"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def crear(orden: OrdenCreate, db: Session = Depends(get_db)):
    return crear_orden(db, orden)


@router.get("/")
def listar(db: Session = Depends(get_db)):
    return obtener_ordenes(db)


@router.get("/{orden_id}")
def obtener(orden_id: int, db: Session = Depends(get_db)):
    return obtener_orden(db, orden_id)


@router.delete("/{orden_id}")
def eliminar(orden_id: int, db: Session = Depends(get_db)):
    return eliminar_orden(db, orden_id)


@router.put("/{orden_id}")
def actualizar(orden_id: int, datos: OrdenCreate, db: Session = Depends(get_db)):
    return orden_crud.actualizar_orden(db, orden_id, datos)

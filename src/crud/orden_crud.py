from sqlalchemy.orm import Session
from src.entities.orden import Orden
from src.schemas.orden_schema import OrdenCreate


def crear_orden(db: Session, orden: OrdenCreate):
    nueva_orden = Orden(fecha=orden.fecha, total=orden.total)
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)
    return nueva_orden


def obtener_orden(db: Session, orden_id: int):
    return db.query(Orden).filter(Orden.id == orden_id).first()


def obtener_ordenes(db: Session):
    return db.query(Orden).all()


def eliminar_orden(db: Session, orden_id: int):
    orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if orden:
        db.delete(orden)
        db.commit()
    return orden


def actualizar_orden(db: Session, orden_id: int, datos: OrdenCreate):
    orden = db.query(Orden).filter(Orden.id == orden_id).first()

    if orden:
        orden.fecha = datos.fecha
        orden.total = datos.total

        db.commit()
        db.refresh(orden)

    return orden

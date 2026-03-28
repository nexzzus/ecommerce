from fastapi import APIRouter

router = APIRouter(prefix="/pago", tags=["Pago"])


@router.get("/")
def listar_pagos():
    return {"mensaje": "listar pagos"}


@router.get("/{pago_id}")
def obtener_pago(pago_id: int):
    return {"mensaje": f"pago {pago_id}"}


@router.post("/")
def crear_pago():
    return {"mensaje": "crear pago"}


@router.put("/{pago_id}")
def actualizar_pago(pago_id: int):
    return {"mensaje": f"actualizar pago {pago_id}"}


@router.delete("/{pago_id}")
def eliminar_pago(pago_id: int):
    return {"mensaje": f"eliminar pago {pago_id}"}

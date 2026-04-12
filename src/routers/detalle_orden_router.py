from fastapi import APIRouter

router = APIRouter(prefix="/detalle_orden", tags=["Detalle Orden"])


@router.get("/")
def listar_detalles():
    return {"mensaje": "listar detalles de orden"}


@router.get("/{detalle_id}")
def obtener_detalle(detalle_id: int):
    return {"mensaje": f"detalle {detalle_id}"}


@router.post("/")
def crear_detalle():
    return {"mensaje": "crear detalle"}


@router.put("/{detalle_id}")
def actualizar_detalle(detalle_id: int):
    return {"mensaje": f"actualizar detalle {detalle_id}"}


@router.delete("/{detalle_id}")
def eliminar_detalle(detalle_id: int):
    return {"mensaje": f"eliminar detalle {detalle_id}"}

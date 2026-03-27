from fastapi import FastAPI
from src.database.database import engine, Base

# IMPORTAR MODELOS (están en entities)
from src.entities import orden
from src.entities import detalle_orden
from src.entities import pago

# IMPORTAR ROUTERS
from src.routers import orden_router
from src.routers import detalle_orden_router
from src.routers import pago_router

app = FastAPI()

# Crear tablas en Neon
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(orden_router.router)
app.include_router(detalle_orden_router.router)
app.include_router(pago_router.router)

@app.get("/")
def inicio():
    return {"mensaje": "API Ecommerce funcionando"}

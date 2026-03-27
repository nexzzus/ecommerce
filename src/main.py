from fastapi import FastAPI
from src.database.database import engine, Base

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

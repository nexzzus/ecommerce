

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.config import engine, Base

from src.entities.users import User
from src.entities.roles import Role
from src.entities.cart_items import CartItem
from src.entities.products import Product
from src.entities.category import Category
from src.entities.discounts import Discount
from src.entities.associations import role_permissions, user_roles, product_categories

import src.routers.orden_router as ord_router
import src.routers.detalle_orden_router as det_router
import src.routers.pago_router as pag_router
from src.api import auth  
from src.core.config import get_settings


app = FastAPI() 
settings = get_settings()

# 1. CONFIGURACIÓN DE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Crear tablas en Neon 
Base.metadata.create_all(bind=engine)

# 3. ROUTERS  
app.include_router(ord_router.router)
app.include_router(det_router.router)
app.include_router(pag_router.router)
app.include_router(auth.router, tags=["Autenticación"])

@app.get("/")
def inicio():
    return {"mensaje": "API Ecommerce funcionando"}

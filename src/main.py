from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.database import engine, Base

from src.entities.users import User
from src.entities.roles import Role
from src.entities.cart_items import CartItem
from src.entities.products import Product
from src.entities.category import Category
from src.entities.discounts import Discount
from src.entities.associations import role_permissions, user_roles, product_categories

from src.routers import orden_router, detalle_orden_router, pago_router
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
app.include_router(orden_router.router)
app.include_router(detalle_orden_router.router)
app.include_router(pago_router.router)
app.include_router(auth.router, tags=["Autenticación"])

@app.get("/")
def inicio():
    return {"mensaje": "API Ecommerce funcionando"}

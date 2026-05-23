from src import entities

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  

from src.core.config import get_settings
from src.core.responses import success_response
from src.database.config import create_tables

from src.api import auth

import src.endpoints.users as users
import src.endpoints.roles as roles
import src.endpoints.permissions as permissions
import src.endpoints.discounts as discounts
import src.endpoints.category as category
import src.endpoints.products as products
import src.endpoints.cart_items as cart_items


try:
    import src.routers.orden_router as orden_router
    import src.routers.detalle_orden_router as detalle_router
    import src.routers.pago_router as pago_router
    TUS_ROUTERS_OK = True
except Exception as e:
    print(f"\n❌ ERROR IMPORTANDO TUS ROUTERS: {e}\n")
    TUS_ROUTERS_OK = False

import src.entities.associations  # noqa: F401
import src.entities.users  # noqa: F401
import src.entities.roles  # noqa: F401
import src.entities.permissions  # noqa: F401
import src.entities.discounts  # noqa: F401
import src.entities.category  # noqa: F401
import src.entities.products  # noqa: F401
import src.entities.cart_items  # noqa: F401


import src.entities.orden  # noqa: F401        

from src.core.exceptions import AppException
from src.core.error_handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from fastapi.exceptions import HTTPException, RequestValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto crea las tablas en Neon al iniciar
    create_tables()
    yield


app = FastAPI(
    title="API Usuarios",
    description="API con FastAPI, SQLAlchemy y PostgreSQL",
    lifespan=lifespan,
)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Routers base del proyecto
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(permissions.router)
app.include_router(discounts.router)
app.include_router(category.router)
app.include_router(products.router)
app.include_router(cart_items.router)
app.include_router(auth.router)


if TUS_ROUTERS_OK:
    app.include_router(orden_router.router)
    app.include_router(detalle_router.router)
    app.include_router(pago_router.router)


@app.get("/")
def inicio():
    return success_response(
        data={"mensaje": "API Ecommerce", "docs": "/docs"},
        message="Bienvenido a la API Ecommerce",
    )
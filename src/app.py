"""

Aplicación FastAPI: API de usuarios, roles y permisos.

Ejecutar con:

  uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

En el lifespan se crean las tablas en la base de datos. Se registran los

routers de users, roles y permissions. Los modelos y tablas de asociación

se importan para que Base.metadata los conozca al llamar create_tables().

"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.responses import success_response
from src.database.config import create_tables

import src.endpoints.users as users
import src.endpoints.roles as roles
import src.endpoints.permissions as permissions
import src.endpoints.discounts as discounts
import src.endpoints.category as category
import src.endpoints.products as products
import src.endpoints.cart_items as cart_items

import src.entities.associations  # noqa: F401

import src.entities.users  # noqa: F401

import src.entities.roles  # noqa: F401

import src.entities.permissions  # noqa: F401

import src.entities.discounts  # noqa: F401

import src.entities.category  # noqa: F401

import src.entities.products  # noqa: F401

import src.entities.cart_items  # noqa: F401

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
    """

    Context manager del ciclo de vida de la app.

    Al iniciar crea las tablas en la base de datos. Al cerrar podría

    ejecutarse lógica de shutdown si fuera necesaria.

    """

    create_tables()

    yield


app = FastAPI(
    title="API Usuarios",
    description="API con FastAPI, SQLAlchemy y PostgreSQL",
    lifespan=lifespan,
)

# manejadores globales de excepciones
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(users.router)

app.include_router(roles.router)

app.include_router(permissions.router)

app.include_router(discounts.router)

app.include_router(category.router)

app.include_router(products.router)

app.include_router(cart_items.router)


@app.get("/")
def inicio():
    return success_response(
        data={"mensaje": "API Ecommerce", "docs": "/docs"},
        message="Bienvenido a la API Ecommerce",
    )

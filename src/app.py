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

from src.database.config import create_tables

from src.endpoints import users, roles, permissions, discounts, categories, products

import src.entities.associations  # noqa: F401

import src.entities.users  # noqa: F401

import src.entities.roles  # noqa: F401

import src.entities.permissions  # noqa: F401

import src.entities.discounts  # noqa: F401

import src.entities.categories  # noqa: F401

import src.entities.products  # noqa: F401


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

app.include_router(users.router)

app.include_router(roles.router)

app.include_router(permissions.router)

app.include_router(discounts.router)

app.include_router(categories.router)

app.include_router(products.router)


@app.get("/")
def inicio():
    """Ruta raíz: mensaje de bienvenida y enlace a la documentación."""

    return {"mensaje": "API Usuarios y E-commerce", "docs": "/docs"}

"""
Configuración de la base de datos PostgreSQL (Neon).

Carga DATABASE_URL desde variables de entorno (.env), crea el motor SQLAlchemy,
la sesión (SessionLocal), la base declarativa (Base) y proporciona get_db
para inyección en FastAPI y create_tables para crear las tablas al arranque.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en las variables de entorno")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "require"},
)

SessionLocal = sessionmaker[Session](autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos para dependencias FastAPI.

    Yields:
        Session: Sesión de SQLAlchemy. Se cierra al salir del scope.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """
    Crea todas las tablas definidas en los modelos registrados en Base.metadata.

    Debe invocarse después de importar todas las entidades y tablas de
    asociación para que existan en el metadata.
    """
    Base.metadata.create_all(bind=engine)

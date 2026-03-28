import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context


# 1. CONFIGURACIÓN DE RUTAS
# Agregamos la raíz del proyecto al path de Python
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

# Importar los archivos desde la estructura 'src'
try:
    from src.database.database import DATABASE_URL
    from src.entities.user import Base
except ImportError:
    # Si falla, intentamos sin el prefijo 'src' (por si acaso)
    sys.path.insert(0, os.path.join(os.getcwd(), "src"))
    from database.database import DATABASE_URL
    from entities.user import Base

# 2. CONFIGURACIÓN DE ALEMBIC
config = context.config

# Interpreta el archivo de configuración para el logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Vinculamos los modelos y la URL de Neon
target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

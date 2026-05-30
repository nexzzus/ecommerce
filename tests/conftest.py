"""
Configuración compartida de pytest.

Define variables de entorno por defecto (mismas que CI) antes de importar la app.
"""

import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg2://test:test@localhost:5432/ecommerce_test",
)
os.environ.setdefault("SSL_MODE", "disable")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key-for-pytest-only-32")

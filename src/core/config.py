"""
Configuración centralizada (JWT, CORS) desde variables de entorno.
En producción: JWT_SECRET_KEY debe ser una cadena larga y aleatoria (p. ej. openssl rand -hex 32).
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ajustes cargados desde el entorno y opcionalmente desde .env"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Orígenes permitidos
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173,"
        "http://127.0.0.1:3000,http://127.0.0.1:5173",
        validation_alias="CORS_ORIGINS",
    )

    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

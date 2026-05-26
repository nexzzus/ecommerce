"""Pruebas de integración HTTP con FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    try:
        from src.app import app
    except ValueError as exc:
        pytest.skip(f"No se pudo cargar la app: {exc}")

    try:
        with TestClient(app) as test_client:
            yield test_client
    except Exception as exc:
        pytest.skip(f"Base de datos no disponible: {exc}")


def test_root_returns_success_envelope(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["mensaje"] == "API Ecommerce"
    assert body["data"]["docs"] == "/docs"


def test_register_requires_valid_payload(client: TestClient):
    response = client.post(
        "/users/register",
        json={"first_name": "A", "last_name": "B"},
    )

    assert response.status_code == 422

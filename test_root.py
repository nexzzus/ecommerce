from fastapi.testclient import TestClient

from src.app import app


def test_root_ok():
    c = TestClient(app)
    r = c.get("/")
    assert r.status_code == 200

    body = r.json()

    assert body.get("success") is True
    assert "data" in body

    data = body["data"]

    assert data.get("mensaje")
    assert data.get("docs") == "/docs"

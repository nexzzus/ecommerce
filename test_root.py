from fastapi.testclient import TestClient

from src.app import app


def test_root_ok():
    c = TestClient(app)
    r = c.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body.get("mensaje")
    assert body.get("docs") == "/docs"

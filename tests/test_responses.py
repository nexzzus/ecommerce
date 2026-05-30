"""Pruebas de las respuestas estándar de la API."""

from src.core.responses import error_response, success_response


def test_success_response_includes_data_and_message():
    result = success_response(data={"id": 1}, message="ok")

    assert result["success"] is True
    assert result["data"] == {"id": 1}
    assert result["message"] == "ok"


def test_success_response_message_can_be_none():
    result = success_response(data=[])

    assert result["success"] is True
    assert result["data"] == []
    assert result["message"] is None


def test_error_response_structure():
    result = error_response(
        code="NOT_FOUND",
        message="Recurso no encontrado",
        details={"field": "id"},
    )

    assert result["success"] is False
    assert result["error"]["code"] == "NOT_FOUND"
    assert result["error"]["message"] == "Recurso no encontrado"
    assert result["error"]["details"] == {"field": "id"}

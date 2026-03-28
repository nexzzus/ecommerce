"""
Cliente HTTP para conectar con los endpoints de la API FastAPI.

Proporciona funciones _get, _post, _put y _delete que usan httpx contra
BASE_URL. Todas levantan excepción en respuestas 4xx/5xx (raise_for_status).
"""

import httpx

BASE_URL = "http://localhost:8000"


def _unwrap(response_json: dict | list) -> dict | list:
    """Extrae el campo 'data' de la respuesta estándar de la API."""
    if (
        isinstance(response_json, dict)
        and response_json.get("success") is True
        and "data" in response_json
    ):
        return response_json["data"]
    return response_json


def _get(url: str, **kwargs) -> dict | list:
    """
    Realiza una petición GET y devuelve el JSON de la respuesta.

    Args:
        url: Ruta relativa al BASE_URL (ej. "/users").
        **kwargs: Argumentos adicionales para httpx (params, headers, etc.).

    Returns:
        Cuerpo de la respuesta como dict o list.

    Raises:
        httpx.HTTPStatusError: Si el status code es 4xx o 5xx.
    """
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.get(url, **kwargs)
        r.raise_for_status()
        return _unwrap(r.json())


def _post(url: str, json: dict, **kwargs) -> dict:
    """
    Realiza una petición POST con cuerpo JSON.

    Args:
        url: Ruta relativa al BASE_URL.
        json: Cuerpo de la petición (será serializado a JSON).
        **kwargs: Argumentos adicionales para httpx.

    Returns:
        Cuerpo de la respuesta como dict, o {} si status 204.
    """
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.post(url, json=json, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return _unwrap(r.json())


def _put(url: str, json: dict, **kwargs) -> dict:
    """
    Realiza una petición PUT con cuerpo JSON.

    Args:
        url: Ruta relativa al BASE_URL.
        json: Cuerpo de la petición.
        **kwargs: Argumentos adicionales para httpx.

    Returns:
        Cuerpo de la respuesta como dict, o {} si status 204.
    """
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.put(url, json=json, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return _unwrap(r.json())


def _delete(url: str, **kwargs) -> None:
    """
    Realiza una petición DELETE.

    Args:
        url: Ruta relativa al BASE_URL.
        **kwargs: Argumentos adicionales para httpx.

    Raises:
        httpx.HTTPStatusError: Si el status code es 4xx o 5xx.
    """
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.delete(url, **kwargs)
        r.raise_for_status()

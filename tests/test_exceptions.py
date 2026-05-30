"""Pruebas de excepciones de aplicación."""

from fastapi import status

from src.core.exceptions import BadRequestError, NotFoundError


def test_not_found_error_has_404_status_and_code():
    err = NotFoundError("User not found")

    assert err.status_code == status.HTTP_404_NOT_FOUND
    assert err.code == "NOT_FOUND"
    assert err.message == "User not found"


def test_bad_request_error_has_400_status():
    err = BadRequestError("Email already registered")

    assert err.status_code == status.HTTP_400_BAD_REQUEST
    assert err.code == "BAD_REQUEST"

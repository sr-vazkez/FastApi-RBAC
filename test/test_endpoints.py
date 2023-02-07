#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json  # noqa
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app import main


client = TestClient(app=main.app)


# Sin loggeo del usuario


@pytest.mark.parametrize("enpoint", [("/redoc"), ("/docs")])
def test_multi_docs_correct(enpoint: str) -> None:
    """Verificamos que los endpoints de docs funcionen.

    Args:
        enpoint (str): endpoint
    """
    response = client.get(enpoint)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "enpoints",
    [
        ("/profile/"),
        ("/users/"),
        ("/users/1"),
        ("/users/searches/"),
        ("/users/searches/"),
        ("/roles/"),
        ("/roles/1"),
        ("/roles/1/users"),
        ("/roles/1/permissions"),
        ("/modules/"),
        ("/modules/1"),
        ("/modules/1/actions"),
        ("/actions/"),
        ("/actions/1"),
        ("/permissions/"),
        ("/permissions/1"),
        ("/auth/refresh"),
    ],
)
def test_protected_get_routes(enpoints: str) -> None:
    """Verificamos acceso a las rutas GET sin loggearnos.

    Args:
        enpoints (str): endpoint
    """
    response = client.get(enpoints)
    assert response.status_code == status.HTTP_421_MISDIRECTED_REQUEST


@pytest.mark.parametrize(
    "enpoints",
    [
        ("/users/create"),
        ("/roles/create"),
        ("/modules/create"),
        ("/actions/create"),
        ("/permissions/assing/actions"),
    ],
)
def test_protected_post_routes(enpoints: str) -> None:
    """Verificamos acceso a las rutas POST sin loggearnos.

    Args:
        enpoints (str): endpoint
    """
    response = client.post(enpoints)
    assert response.status_code == status.HTTP_421_MISDIRECTED_REQUEST


@pytest.mark.parametrize(
    "enpoints",
    [("/users/1"), ("/roles/1"), ("/modules/1"), ("/actions/1"), ("/permissions/1")],
)
def test_protect_put_routes(enpoints: str) -> None:
    """Verificamos acceso a las rutas PUT sin loggearnos.

    Args:
        enpoints (str): endpoint
    """
    response = client.put(enpoints)
    assert response.status_code == status.HTTP_421_MISDIRECTED_REQUEST


@pytest.mark.parametrize(
    "enpoints",
    [
        ("/profile/update/password"),
        ("/users/1/update/passwords"),
    ],
)
def test_protect_patch_routes(enpoints: str) -> None:
    """Verificamos acceso a las rutas PATCH sin loggearnos.

    Args:
        enpoints (str): enpoint
    """
    response = client.patch(enpoints)
    assert response.status_code == status.HTTP_421_MISDIRECTED_REQUEST


@pytest.mark.parametrize(
    "enpoints",
    [
        ("/users/1/delete/"),
        ("/roles/1/delete/"),
        ("/modules/1/delete/"),
        ("/actions/1/delete/"),
        ("/permissions/1/delete/"),
    ],
)
def test_protect_delete_routes(enpoints: str) -> None:
    """Verificamos acceso a las rutas DELETE sin loggearnos.

    Args:
        enpoints (str): endpoint
    """
    response = client.delete(enpoints)
    assert response.status_code == status.HTTP_421_MISDIRECTED_REQUEST


@pytest.mark.parametrize(
    "enpoints",
    [
        ("/users/1/delete/"),
        ("/roles/1/delete/"),
        ("/modules/1/delete/"),
        ("/actions/1/delete/"),
        ("/permissions/1/delete/"),
        ("/profile/update/password"),
        ("/users/1/update/passwords"),
        ("/users/1"),
        ("/roles/1"),
        ("/modules/1"),
        ("/actions/1"),
        ("/permissions/1"),
    ],
)
def test_not_exist_method(enpoints: str) -> None:
    """Verificamos acceso a rutas que no existen dicho metodo.

    Args:
        enpoints (str): enpoint.
    """
    response = client.post(enpoints)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize(
    "endpoints",
    [
        ("logout"),
        ("/some_endpoint"),
        ("/login"),
        ("/user"),
        ("/admin"),
        ("/registers"),
    ],
)
def test_not_exist_endpoint(endpoints: str) -> None:
    """Verificamos acceso a rutas que no existen dicho enpoint.

    Comporbamos la seguridad

    Args:
        endpoints (str): definimos la ruta la cual hara el test.
    """
    response = client.get(endpoints)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "email, password",
    [
        ("otrouser@gmail.com", "somepassword"),
        ("otrouser@hotmail.com", "$nb8&LkNEH&tgy7!K"),
        ("test_admin@gmail.com", "$nb8&LkNEH&tgy7!K"),
        ("test_admin@palme.com", "test_admin"),
        ("admin@palmer.com", "test_password"),
        ("admin@palmer.com", "admin123"),
        ("polo@usa.c", "8uscX&6gQEs4!cLU#"),
        ("robert@u.c", "8uscX&6gQEs4!cLU#"),
        (
            "johndoe@example.com",
            "g@Fb6QebgMqdGvmXZT#8^b&7XFj^YCsTbUs&Ne",
        ),
    ],
)
def test_login_invalid_credentials(email: str, password: str) -> None:
    """Validamos login con credenciales invalidas.

    Args:
        email (str): email
        password (str): password
    """
    user = {"email": email, "password": password}
    response = client.post("/auth/signing", json=user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "email, password",
    [
        # Invalid formats for emails
        ("otrouser@.com", "8uscX&6gQEs4!cLU#"),
        ("@emaple.com", "8uscX&6gQEs4!cLU#"),
        ("johndoe@example", "8uscX&6gQEs4!cLU#"),
        ("johndoe@examplecom", "8uscX&6gQEs4!cLU#"),
        ("@emaple.com", "8uscX&6gQEs4!cLU#"),
        # Invalid formats for password
        ("admin@palmer.com", "8"),
        ("admin@palmer.com", "cinco"),
        ("josua@emaple.com", "1234567"),
        ("josua@facebook.com", "qwerty"),
    ],
)
def test_login_invalid_request_login(email: str, password: str) -> None:
    """Validamos login con formatos invalidos.

    Args:
        email (str): email field
        password (str): password field
    """
    user = {"email": email, "password": password}
    response = client.post("/auth/signing", json=user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

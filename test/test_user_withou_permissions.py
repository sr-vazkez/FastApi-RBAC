#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json  # noqa
from typing import Any, Generator


import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


from app import main
from app.database.main import SessionLocal
from app.models.roles import Role
from app.models.users import Users


from app.extras.hashing import Hash


client = TestClient(app=main.app)


@pytest.fixture(scope="module")
def setup() -> Generator[Session, None, None]:
    """Inicialiamos conexion a la bd.

    Yields:
        Generator[Session, None, None]: Se genera un hilo.
    """
    # setup conexion
    db = SessionLocal()
    yield db
    # teardown
    delete_user = db.query(Users).filter(Users.email == "test_user@palmer.com")
    delete_user.delete(synchronize_session=False)
    delete_role = db.query(Role).filter(Role.name == "test_user")
    delete_role.delete(synchronize_session=False)
    db.commit()
    db.close()


def test_create_all(setup) -> None:
    """Creamos un usuario sin permisos.

    Args:
        setup (Conexion BD): Traemos el hilo como parametro pa realizar consultas.
    """
    role = Role(
        id="542e78b6-16bc-445a-8f7d-208914f67e3e",
        name="test_user",
        description="test_user",
    )
    setup.add(role)
    setup.commit()
    user = Users(
        id="3520c0d0-35a3-4caf-803f-0e162ba1ef8e",
        email="test_user@palmer.com",
        password=Hash().bcrypt("test_password"),
        is_active=True,
        role_id="542e78b6-16bc-445a-8f7d-208914f67e3e",
    )
    setup.add(user)
    setup.commit()


@pytest.fixture()
def setUpToken() -> Generator[dict[str, Any], None, None]:
    """Generamos un token.

    Yields:
        Generator[dict[str, Any], None, None]: Generamos un hilo el cual contiene el token.
    """
    login_admin_user = {"email": "test_user@palmer.com", "password": "test_password"}
    response = client.post("/auth/signing", json=login_admin_user)
    header_user = {"Authorization": "Bearer " + response.json()["data"]["access_token"]}
    yield header_user


@pytest.fixture()
def setUpRefreshToken() -> Generator[dict[str, Any], None, None]:
    """Generamos un refresh token.

    Yields:
        Generator[dict[str, Any], None, None]: Generamos un hilo el cual
         contiene el refresh token.
    """
    login_admin_user = {"email": "test_admin@gmail.com", "password": "test_password"}
    response = client.post("/auth/signing", json=login_admin_user)
    header_refresh_user = {
        "Authorization": "Bearer " + response.json()["data"]["refresh_token"]
    }
    yield header_refresh_user


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/"),
        ("/users/?start=0&limit=16"),
        ("/users/?start=16&limit=32"),
        ("/roles/"),
        ("/roles/?start=0&limit=16"),
        ("/roles/?start=16&limit=32"),
        ("/modules/"),
        ("/modules/?start=0&limit=16"),
        ("/modules/?start=16&limit=32"),
        ("/permissions/"),
        ("/permissions/?start=0&limit=16"),
        ("/permissions/?start=16&limit=32"),
        ("/actions/"),
        ("/actions/?start=0&limit=16"),
        ("/actions/?start=16&limit=32"),
    ],
)
def test_all_gets_endpoints_without_permissions(setUpToken, endpoint) -> None:
    """Verificamos si un usuario sin permissos puede acceder a endpoints protegidos.

    Args:
        setUpToken (Token): Hilo con el JWT.
        endpoint (str): ruta de accesso.
    """
    header = setUpToken
    response = client.get(endpoint, headers=header)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/create"),
        ("/roles/create"),
        ("/modules/create"),
        ("/actions/create"),
        ("/permissions/assing/actions"),
    ],
)
def test_all_post_endpoints_without_permissions(setUpToken, endpoint) -> None:
    """Verificamos acceso a las rutas POST sin permisos.

    Args:
        setUpToken (Token): Hilo con el JWT.
        endpoint (str): ruta de accesso.
    """
    header = setUpToken
    response = client.post(endpoint, headers=header)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/cb382af6-6b5c-4e4c-8498-0b82449a3ff7"),
        ("/users/cb382af6-6b5c-4e4c-8498-0a3ff7"),
        ("/roles/cce2b0fd-3e7b-4d07-b4e6-e5293a0d2270"),
        ("/roles/@@#¢-3e7b-4d07-b4e6-e5293a0d2270"),
        ("/modules/ecc57911-4689-4135-b2ac-370308f689ee"),
        ("/modules/some-string-okidoki-okidoki"),
        ("/actions/3c3d02fa-7cad-41b7-b4d4-cd28bed3f2ea"),
        ("/actions/create-3c3d02fa-7cad-41b7-b4d4-cd28bed3f2ea"),
        ("/permissions/ecc57911-4689-4135-b2ac-370308f689ee"),
        ("/permissions/ce3dac7d-6d66-47b2-97f0-109432132d67"),
    ],
)
def test_all_put_endpoints_without_permissions(setUpToken, endpoint) -> None:
    """Verificamos acceso a las rutas PUT sin permisos.

    Args:
        setUpToken (Token): Hilo con el JWT.
        endpoint (str): ruta de accesso.
    """
    header = setUpToken
    response = client.put(endpoint, headers=header)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/d2dd4631-5834-4b80-8211-ba36f53579bc/delete/"),
        ("/users/98d605e-772b-11ed-a1eb-0242ac120002/delete/"),
        ("/roles/7e754429-524f-47da-a096-30d6dfe459ab/delete/"),
        ("/roles/7b5fce25-894f-4fbf-a188-d91983456a4c/delete/"),
        ("/modules/c9485205-13bb-4f7e-8849-a2cc3fa4bded/delete/"),
        ("/modules/dbe47277-52cb-4c01-9673-d1a8956ec105/delete/"),
        ("/permissions/b4312971-ea91-4caf-ae97-115d39f5b873/delete/"),
        ("/permissions/522d8aee-b61b-418b-b436-c2bdc2153812/delete/"),
        ("/actions/d66260dc-ac1a-45df-b815-7e7080d14413/delete/"),
        ("/actions/2336204a-9284-4366-8d56-63ae444adaa1/delete/"),
    ],
)
def test_all_delete_endpoints_without_permissions(setUpToken, endpoint) -> None:
    """Verificamos acceso a las rutas DELETE sin permisos.

    Args:
        setUpToken (Token): Hilo con el JWT.
        endpoint (str): ruta de accesso.
    """
    header = setUpToken
    response = client.delete(endpoint, headers=header)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/cfbb6369-8d27-430d-93e9-99c3a6f7d27f/update/passwords"),
        ("/users/3520c0d0-35a3-4caf-803f-0e162ba1ef8e/update/passwords"),
    ],
)
def test_all_patch_endpoints_without_permissions(setUpToken, endpoint) -> None:
    """Verificamos acceso a las rutas PATCH sin permisos.

    Args:
        setUpToken (Token): Hilo con el JWT.
        endpoint (str): ruta de accesso.
    """
    header = setUpToken
    response = client.patch(endpoint, headers=header)
    assert response.status_code == status.HTTP_403_FORBIDDEN

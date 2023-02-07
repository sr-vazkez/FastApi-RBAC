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
from app.models.module import Module
from app.models.actions import Actions
from app.models.role_actions import Role_Actions
from app.extras.hashing import Hash


client = TestClient(app=main.app)


@pytest.fixture(scope="module")
def setup() -> Generator[Session, None, None]:
    """Generamos conexion y borramos todo al final.

    Yields:
        Generator[Session, None, None]: Conexion a la BD.
    """
    # setup conexion
    db = SessionLocal()
    yield db
    # teardown
    delete_role_actions = db.query(Role_Actions).all()
    for item in delete_role_actions:
        db.delete(item)
    db.flush()

    delete_actions = db.query(Actions).all()
    for a in delete_actions:
        db.delete(a)
        db.flush()
    db.commit()

    delete_modules = db.query(Module).all()
    for m in delete_modules:
        db.delete(m)
        db.flush()
    db.commit()

    delete_user = db.query(Users).all()
    for u in delete_user:
        db.delete(u)
        db.flush()
    db.commit()

    delete_role = db.query(Role).all()
    for r in delete_role:
        db.delete(r)
        db.flush()
    db.commit()


def test_create_all(setup) -> None:
    """Creamos todo de forma no dinamica.

    Args:
        setup (Yield): Conexion a la BD
    """
    all_actions = [
        Role(
            id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            name="test_admin",
            description="test_admin",
        ),
        Users(
            id="3520c0d0-35a3-4caf-803f-0e162ba1ef8e",
            email="test_admin@gmail.com",
            password=Hash().bcrypt("test_password"),
            is_active=True,
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
        ),
        Users(
            id="bb9e8a8a-053f-4f94-a2d9-ee22dac6583c",
            email="delete_admin@palmer.com",
            password=Hash().bcrypt("test_password"),
            is_active=True,
            is_deleted=True,
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
        ),
        Module(
            id="446d0bd7-cfc7-4a89-8767-080d844e1453",
            name="users",
            description="module for Users",
        ),
        Module(
            id="dd50cb81-2a93-4e6f-8efc-5044746f5a7b",
            name="roles",
            description="module for Roles",
        ),
        Module(
            id="fd9affdf-d132-48fe-8105-2c026462fe3f",
            name="actions",
            description="module for Actions",
        ),
        Module(
            id="e5cf5b44-2724-46c2-b01d-0d036d5af741",
            name="modules",
            description="module for modules",
        ),
        Module(
            id="8791a275-4554-448e-a825-951b3d796c73",
            name="permissions",
            description="module for Permissions",
        ),
        Actions(
            id="ba7bf92e-4f7c-4534-b8b1-e40e545857f3",
            action_name="create",
            is_active=True,
            description="create action for permissions module",
            module_id="8791a275-4554-448e-a825-951b3d796c73",
        ),
        Actions(
            id="5b0f3a3a-dc8c-4783-a826-bb8003651496",
            action_name="read",
            is_active=True,
            description="read action for permissions module",
            module_id="8791a275-4554-448e-a825-951b3d796c73",
        ),
        Actions(
            id="ce1b8280-13a0-4416-b83d-2db116469edc",
            action_name="update",
            is_active=True,
            description="update action for permissions module",
            module_id="8791a275-4554-448e-a825-951b3d796c73",
        ),
        Actions(
            id="bcf023cf-9d79-4aaa-83fa-8d3db7d1591c",
            action_name="delete",
            is_active=True,
            description="delete action for permissions module",
            module_id="8791a275-4554-448e-a825-951b3d796c73",
        ),
        Actions(
            id="c909c7a3-df89-43ad-9d01-47da265582fd",
            action_name="create",
            is_active=True,
            description="create action for modules module",
            module_id="e5cf5b44-2724-46c2-b01d-0d036d5af741",
        ),
        Actions(
            id="b4d8ab12-da62-4cbb-9108-9d95bc27c8ea",
            action_name="read",
            is_active=True,
            description="read action for modules module",
            module_id="e5cf5b44-2724-46c2-b01d-0d036d5af741",
        ),
        Actions(
            id="41383eac-3fdb-45f1-9313-a1b3cfb6e13a",
            action_name="update",
            is_active=True,
            description="update action for modules module",
            module_id="e5cf5b44-2724-46c2-b01d-0d036d5af741",
        ),
        Actions(
            id="83078c23-a691-48f6-be30-f2452de94faa",
            action_name="delete",
            is_active=True,
            description="delete action for modules module",
            module_id="e5cf5b44-2724-46c2-b01d-0d036d5af741",
        ),
        Actions(
            id="9d49814d-74f3-43fc-a09e-dfac24b5d912",
            action_name="create",
            is_active=True,
            description="create action for actions module",
            module_id="fd9affdf-d132-48fe-8105-2c026462fe3f",
        ),
        Actions(
            id="f7df9643-8ede-448a-8150-89b799720f1b",
            action_name="read",
            is_active=True,
            description="read action for actions module",
            module_id="fd9affdf-d132-48fe-8105-2c026462fe3f",
        ),
        Actions(
            id="fb5b35a6-6b7d-4a49-8413-0f357dd7602c",
            action_name="update",
            is_active=True,
            description="update action for actions module",
            module_id="fd9affdf-d132-48fe-8105-2c026462fe3f",
        ),
        Actions(
            id="d3e5dddb-be5a-4229-a3cd-db10a1220eae",
            action_name="delete",
            is_active=True,
            description="delete action for actions module",
            module_id="fd9affdf-d132-48fe-8105-2c026462fe3f",
        ),
        Actions(
            id="836931ec-3c29-4e7e-87cb-ac69d444e5cc",
            action_name="create",
            is_active=True,
            description="create action for roles module",
            module_id="dd50cb81-2a93-4e6f-8efc-5044746f5a7b",
        ),
        Actions(
            id="3365aa30-a81c-45c7-9853-a586bf03ed7f",
            action_name="read",
            is_active=True,
            description="read action for roles module",
            module_id="dd50cb81-2a93-4e6f-8efc-5044746f5a7b",
        ),
        Actions(
            id="65d9d5bf-3867-4dd2-a2a0-03f2ad8a28e8",
            action_name="update",
            is_active=True,
            description="update action for roles module",
            module_id="dd50cb81-2a93-4e6f-8efc-5044746f5a7b",
        ),
        Actions(
            id="825e7d13-f021-485a-88d6-57e4127c4448",
            action_name="delete",
            is_active=True,
            description="delete action for roles module",
            module_id="dd50cb81-2a93-4e6f-8efc-5044746f5a7b",
        ),
        Actions(
            id="35e2d961-eb85-4043-b57c-f0021947d61d",
            action_name="create",
            is_active=True,
            description="create action for users module",
            module_id="446d0bd7-cfc7-4a89-8767-080d844e1453",
        ),
        Actions(
            id="2662c1c8-808c-49b4-825a-8a845fd027e6",
            action_name="read",
            is_active=True,
            description="read action for users module",
            module_id="446d0bd7-cfc7-4a89-8767-080d844e1453",
        ),
        Actions(
            id="3e93b3f6-7626-482d-8a1c-31d162d6ba72",
            action_name="update",
            is_active=True,
            description="update action for users module",
            module_id="446d0bd7-cfc7-4a89-8767-080d844e1453",
        ),
        Actions(
            id="14aaf050-339b-45f0-a097-741faafcbae6",
            action_name="delete",
            is_active=True,
            description="delete action for users module",
            module_id="446d0bd7-cfc7-4a89-8767-080d844e1453",
        ),
        Role_Actions(
            id="263526ce-17e2-4b55-b979-0e7d17afaaa7",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="ba7bf92e-4f7c-4534-b8b1-e40e545857f3",
        ),
        Role_Actions(
            id="3b02860d-176f-43bd-ab71-25523db36f63",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="5b0f3a3a-dc8c-4783-a826-bb8003651496",
        ),
        Role_Actions(
            id="f2f81de9-9216-44ab-8aff-676dd95b681c",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="ce1b8280-13a0-4416-b83d-2db116469edc",
        ),
        Role_Actions(
            id="05135adf-e151-4de8-b06e-e77d02ded2a1",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="bcf023cf-9d79-4aaa-83fa-8d3db7d1591c",
        ),
        Role_Actions(
            id="9e16edc3-3a04-426d-b554-643e1dd7c33c",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="c909c7a3-df89-43ad-9d01-47da265582fd",
        ),
        Role_Actions(
            id="e68d1c5b-41ab-43b1-bf29-a5939cf5ef88",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="b4d8ab12-da62-4cbb-9108-9d95bc27c8ea",
        ),
        Role_Actions(
            id="0856b564-995d-4d22-9f9a-aad549cfa177",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="41383eac-3fdb-45f1-9313-a1b3cfb6e13a",
        ),
        Role_Actions(
            id="fa0c8080-bbf7-4561-a500-b74f67343c0d",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="83078c23-a691-48f6-be30-f2452de94faa",
        ),
        Role_Actions(
            id="272427c7-7b4a-49b7-9019-af2c867913ca",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="9d49814d-74f3-43fc-a09e-dfac24b5d912",
        ),
        Role_Actions(
            id="8fc3cb9c-3a1c-4635-a558-0fcdb67a909e",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="f7df9643-8ede-448a-8150-89b799720f1b",
        ),
        Role_Actions(
            id="42eb962f-66c3-4d01-a5dc-1ee523270f9d",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="fb5b35a6-6b7d-4a49-8413-0f357dd7602c",
        ),
        Role_Actions(
            id="6f4a766d-7d5f-48e6-b297-3467076de0a1",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="d3e5dddb-be5a-4229-a3cd-db10a1220eae",
        ),
        Role_Actions(
            id="3f648668-25f4-4ee5-95ca-964c00fbc9a2",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="836931ec-3c29-4e7e-87cb-ac69d444e5cc",
        ),
        Role_Actions(
            id="9e176d8f-5c9a-4bc2-b521-b097ae828bac",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="3365aa30-a81c-45c7-9853-a586bf03ed7f",
        ),
        Role_Actions(
            id="47acaa9a-6f73-4e2b-8a6c-357b876f6e48",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="65d9d5bf-3867-4dd2-a2a0-03f2ad8a28e8",
        ),
        Role_Actions(
            id="9bf5eb74-9e87-4457-96a7-5b2958eff1e7",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="825e7d13-f021-485a-88d6-57e4127c4448",
        ),
        Role_Actions(
            id="6b35b0e5-1b77-48c2-919b-49c2a6286fdb",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="35e2d961-eb85-4043-b57c-f0021947d61d",
        ),
        Role_Actions(
            id="573ca33b-bdfe-4785-bfff-3536de5b6404",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="2662c1c8-808c-49b4-825a-8a845fd027e6",
        ),
        Role_Actions(
            id="977b05e2-beb3-40cb-8cda-9d921f95ef35",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="3e93b3f6-7626-482d-8a1c-31d162d6ba72",
        ),
        Role_Actions(
            id="9ae22552-34d7-4b0a-8dab-6bcf80511e43",
            role_id="4e5a506c-1973-4cf6-ae52-716ecf4cb239",
            actions_id="14aaf050-339b-45f0-a097-741faafcbae6",
        ),
    ]

    setup.bulk_save_objects(all_actions)
    setup.commit()


@pytest.mark.parametrize(
    "email, password", [("test_admin@gmail.com", "test_password")]
)
def test_login_valid_credentials(email: str, password: str) -> None:
    """Verificamos login con credenciales validas.

    Args:
        email (str): email for a user
        password (str): password for a user
    """
    user = {"email": email, "password": password}
    response = client.post("/auth/signing", json=user)
    assert response.status_code == status.HTTP_200_OK


@pytest.fixture()
def setUpToken() -> Generator[dict[str, Any], None, None]:
    """Generamos un token.

    Yields:
        Generator[dict[str, Any], None, None]: Generamos un hilo el cual contiene el token.
    """
    login_admin_user = {"email": "test_admin@gmail.com", "password": "test_password"}
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


def test_refresh_token(setUpRefreshToken) -> None:
    """Verificamos si funciona el Refresh Token.

    Args:
        setUpRefreshToken (Yield): Refresh Token
    """
    header = setUpRefreshToken
    response = client.get("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_200_OK


def test_user_profile(setUpToken):
    """Verificamos la informacion del usuario.

    Args:
        setUpToken (Yield): Token
    """
    header = setUpToken
    response = client.get("/profile", headers=header)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/?start=asdjhhg&limit=asdasd"),
        ("/users/?start=0&limit=asdasd"),
        ("/users/?start=whdjgasd&limit=16"),
        ("/roles/?start=r0&limit=16"),
        ("/roles/?start=ttt16&limit=32"),
        ("/modules/?start=0&limit=16hjbjh"),
        ("/modules/?start=16&limit=3nn2"),
        ("/modules/708c210d-1482-4a25-aac1-51ba4941/actions/?start=16&limit=3nn2"),
        ("/modules/708c210d-1482-4a25-aac1-51ba4941/actions/?start=16b&limit=32"),
        ("/permissions/?start=0&limit=1·"),
        ("/permissions/?start=##&limit=32"),
        ("/actions/?start===&limit=16"),
        ("/actions/?start===16&limit=32"),
    ],
)
def test_get_all_items_bad_queries_params(setUpToken, endpoint) -> None:
    """Verificamos validaciones en parametros de queries en rutas GET.

    Args:
        setUpToken (Yield): Token
        endpoint (str): ruta a la cual se ejecutara el test.
    """
    header = setUpToken
    response = client.get(endpoint, headers=header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/"),
        ("/users/?start=0&limit=16"),
        ("/users/?start=16&limit=32"),
        ("/roles/"),
        ("/roles/?start=0&limit=16"),
        ("/roles/?start=16&limit=32"),
        ("/roles/4e5a506c-1973-4cf6-ae52-716ecf4cb239/users?start=16&limit=32"),
        ("/roles/4e5a506c-1973-4cf6-ae52-716ecf4cb239/users?start=32&limit=48"),
        ("/modules/"),
        ("/modules/?start=0&limit=16"),
        ("/modules/?start=16&limit=32"),
        ("/modules/446d0bd7-cfc7-4a89-8767-080d844e1453/actions?start=0&limit=16"),
        ("/modules/446d0bd7-cfc7-4a89-8767-080d844e1453/actions?start=16&limit=32"),
        ("/permissions/"),
        ("/permissions/?start=0&limit=16"),
        ("/permissions/?start=16&limit=32"),
        ("/actions/"),
        ("/actions/?start=0&limit=16"),
        ("/actions/?start=16&limit=32"),
    ],
)
def test_get_all_items(setUpToken, endpoint) -> None:
    """Verificamos obtencion de datos en rutas GET.

    Args:
        setUpToken (Yield): Token
        endpoint (str): ruta a la cual se ejecutara el test.
    """
    header = setUpToken
    response = client.get(endpoint, headers=header)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/3520c0d0-35a3-4caf-803f-0e162ba1ef8e"),
        ("/roles/4e5a506c-1973-4cf6-ae52-716ecf4cb239"),
        ("/modules/446d0bd7-cfc7-4a89-8767-080d844e1453"),
        # ('/permissions/b93ad4c7-1590-407f-b311-7266b7f3989a'),
    ],
)
def test_get_one_item(setUpToken, endpoint) -> None:
    """Verificamos la obtencion de un objeto en rutas GET.

    Args:
        setUpToken (Yield): Token
        endpoint (str): ruta a la cual se ejecutara el test.
    """
    header = setUpToken
    response = client.get(endpoint, headers=header)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/5bd962ba-0a4f-4d86-ab58-265d5a87f3cd"),
        ("/users/b0365aec-e1d5-4aa2-8fed-22dbd31fef58"),
        ("/roles/bc838273-b035-4bf4-99ec-d660e1ba6f49"),
        ("/roles/160af225-3b55-4fb0-8a8f-989ebff29eac"),
        ("/modules/e3a3c8b6-9206-401f-a1da-cc14705c75dc"),
        ("/modules/708c210d-1482-4a25-aac1-51ba494110df"),
        ("/actions/73e46ed9-c3c2-47bb-ab59-670d3899923e"),
        ("/actions/5cef3a61-b2ed-47a2-a33b-eaaced2a37fc"),
        ("/permissions/2c97dbf5-b92f-4d36-a521-f91278c3568b"),
        ("/permissions/5a8dc5b2-4174-482a-b900-49ace01c0752"),
    ],
)
def test_get_one_item_fail(setUpToken, endpoint) -> None:
    """Verificamos la validaion al obtener un objeto en rutas GET.

    Args:
        setUpToken (Yield): Token
        endpoint (str): ruta a la cual se ejecutara el test.
    """
    header = setUpToken
    response = client.get(endpoint, headers=header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/5bd962ba-0a4-4d86-ab58-265d5a87f3cd"),
        ("/users/b0365aec-e1d5-4aa2-8fed-2dbd31fef58"),
        ("/roles/bc873-b035-4bf4-99ec-d660e1ba6f49"),
        ("/roles/160af225-3b55-4fb0-8a8f-9bff29eac"),
        ("/modules/e3a3c8b6-9206-401f-a1da-xdsfghj"),
        ("/modules/708c210d-1482-4a25-aac1-51ba4941"),
        ("/modules/708c210d-1482-4a25-aac1-51ba4941/actions/"),
        ("/actions/73e46ed9-c3c2-47bb-ab5@@9-670d3899923e"),
        ("/actions/5cs33b-ed2a37fc"),
        ("/permissions/2c97dbf521f91278c356b"),
        ("/permissions/5a"),
    ],
)
def test_get_one_item_fail_format(setUpToken, endpoint) -> None:
    """Verificamos la validaion del UUID al obtener un objeto en rutas GET.

    Args:
        setUpToken (Yield): Token
        endpoint (str): ruta a la cual se ejecutara el test.
    """
    header = setUpToken
    response = client.get(endpoint, headers=header)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


""" 
@pytest.mark.parametrize(
    "endpoint", [
        ('/users/create'),
        ('/roles/create'),
        ('/modules/create'),
        ('/actions/create'),
        ('/permissions/assing/actions'),
    ]
)
def test_all_post_endpoints(
        setUpToken,
        endpoint
    ) -> None:
    header = setUpToken
    response = client.post(endpoint,headers=header)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.parametrize(
    "endpoint", [
        ('/users/cb382af6-6b5c-4e4c-8498-0b82449a3ff7'),
        ('/users/cb382af6-6b5c-4e4c-8498-0a3ff7'),
        ('/roles/cce2b0fd-3e7b-4d07-b4e6-e5293a0d2270'),
        ('/roles/@@#¢-3e7b-4d07-b4e6-e5293a0d2270'),
        ('/modules/ecc57911-4689-4135-b2ac-370308f689ee'),
        ('/modules/some-string-okidoki-okidoki'),
        ('/actions/3c3d02fa-7cad-41b7-b4d4-cd28bed3f2ea'),
        ('/actions/create-3c3d02fa-7cad-41b7-b4d4-cd28bed3f2ea'),
        ('/permissions/ecc57911-4689-4135-b2ac-370308f689ee'),
        ('/permissions/ce3dac7d-6d66-47b2-97f0-109432132d67'),
    ]
)
def test_all_put_endpoints(
        setUpToken,
        endpoint
    ) -> None:
    header = setUpToken
    response = client.put(endpoint,headers=header)
    assert response.status_code == status.HTTP_403_FORBIDDEN
@pytest.mark.parametrize(
    "endpoint", [
        ('/users/cfbb6369-8d27-430d-93e9-99c3a6f7d27f/update/passwords'),
        ('/users/3520c0d0-35a3-4caf-803f-0e162ba1ef8e/update/passwords'),
    ]
)
def test_all_patch_endpoints(
        setUpToken,
        endpoint
    ) -> None:
    header = setUpToken
    response = client.patch(endpoint,headers=header)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "endpoint", [
        ('/users/d2dd4631-5834-4b80-8211-ba36f53579bc/delete/'),
        ('/users/98d605e-772b-11ed-a1eb-0242ac120002/delete/'),
        ('/roles/7e754429-524f-47da-a096-30d6dfe459ab/delete/'),
        ('/roles/7b5fce25-894f-4fbf-a188-d91983456a4c/delete/'),
        ('/modules/c9485205-13bb-4f7e-8849-a2cc3fa4bded/delete/'),
        ('/modules/dbe47277-52cb-4c01-9673-d1a8956ec105/delete/'),
        ('/permissions/b4312971-ea91-4caf-ae97-115d39f5b873/delete/'),
        ('/permissions/522d8aee-b61b-418b-b436-c2bdc2153812/delete/'),
        ('/actions/d66260dc-ac1a-45df-b815-7e7080d14413/delete/'),
        ('/actions/2336204a-9284-4366-8d56-63ae444adaa1/delete/'),
    ]
)
def test_all_delete_endpoints(
        setUpToken,
        endpoint
    ) -> None:
    header = setUpToken
    response = client.delete(endpoint,headers=header)
    assert response.status_code == status.HTTP_403_FORBIDDEN
"""


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/create"),
    ],
)
def test_make_one_user_ok(setUpToken, endpoint):
    """Validando verificacion de creacion de un usuario con role valido.

    Args:
        setUpToken (Yield): Token
        endpoint (str): Endpoint
    """
    header = setUpToken
    new_user = {
        "email": "otro_user@spuky.com",
        "password": "446d0bd7-cfc7-4a89-8767-080d844e1453",
        "role_id": "446d0bd7-cfc7-4a89-8767-080d844e1453",
        "is_active": True,
    }
    response = client.post(endpoint, headers=header, json=new_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "endpoint",
    [
        ("/users/create"),
    ],
)
def test_created_user_delete(setUpToken, endpoint):
    """Validando si un usuario eliminado es restaurado.

    Args:
        setUpToken (Yield): Token
        endpoint (str): Endpoint
    """
    header = setUpToken
    new_user = {
        "email": "delete_admin@palmer.com",
        "password": "446d0bd7-cfc7-4a89-8767-080d844e1453",
        "role_id": "4e5a506c-1973-4cf6-ae52-716ecf4cb239",
        "is_active": True,
    }
    response = client.post(endpoint, headers=header, json=new_user)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize(
    "endpoint", [("/users/delete/bb9e8a8a-053f-4f94-a2d9-ee22dac6583c")]
)
def test_delete_user_fail(setUpToken, endpoint):
    """Validando verificacion de GUIIDS.

    Args:
        setUpToken (Yield): Token
        endpoint (str): Endpoint
    """
    header = setUpToken
    response = client.delete(endpoint, headers=header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


#


@pytest.mark.parametrize(
    "actual_password, new_password, password_confirmation",
    [
        ("1234567890", "qwertyuiop", "1234567890"),
        ("test_password", "qwertyuiop", "1234567890"),
        ("strangepassword", "1234567890", "12345678s0"),
        ("another2134234password", "1267890", "12345678s0"),
    ],
)
def test_user_update_self_password_fail(
    setUpToken, actual_password: str, new_password: str, password_confirmation: str
) -> None:
    """Verificamos la validacion al modificar un password.

    Args:
        setUpToken (Yield): Token
        actual_password (str): ingresa el passowrd actual
        new_password (str): Ingresa el nuevo password
        password_confirmation (str): Confirma el password anterior
    """
    header = setUpToken
    data = {
        "actual_password": actual_password,
        "new_password": new_password,
        "password_confirmation": password_confirmation,
    }
    response = client.patch("/profile/update/password", headers=header, json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "actual_password, new_password, password_confirmation",
    [
        ("qwertyuiop", "1234567890", "1234567890"),
        ("strangepassword", "1234567890", "1234567890"),
    ],
)
def test_user_update_self_password_invalid_credentials(
    setUpToken, actual_password: str, new_password: str, password_confirmation: str
) -> None:
    """Verificamos la validacion al modificar un password.

    Args:
        setUpToken (Yield): Token
        actual_password (str): ingresa el passowrd actual
        new_password (str): Ingresa el nuevo password
        password_confirmation (str): Confirma el password anterior
    """
    header = setUpToken
    data = {
        "actual_password": actual_password,
        "new_password": new_password,
        "password_confirmation": password_confirmation,
    }
    response = client.patch("/profile/update/password", headers=header, json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "actual_password, new_password, password_confirmation",
    [
        ("test_password", "1234567890", "1234567890"),
    ],
)
def test_user_update_self_password_fine(
    setUpToken, actual_password: str, new_password: str, password_confirmation: str
) -> None:
    """Verificamos la funcionalidad al modificar un password.

    Args:
        setUpToken (Yield): Token
        actual_password (str): ingresa el passowrd actual
        new_password (str): Ingresa el nuevo password
        password_confirmation (str): Confirma el password anterior
    """
    header = setUpToken
    data = {
        "actual_password": actual_password,
        "new_password": new_password,
        "password_confirmation": password_confirmation,
    }
    response = client.patch("/profile/update/password", headers=header, json=data)
    assert response.status_code == status.HTTP_202_ACCEPTED

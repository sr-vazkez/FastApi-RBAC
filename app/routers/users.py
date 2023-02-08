from typing import Optional, Union
from uuid import UUID

from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.dependencies.data_conexion import get_db
from app.dependencies.permissions_policy import (
    users_create,
    users_read,
    users_update,
    users_delete,
)
from app.internal.users import UsersActions
from app.schemas import schemas_config
from app.schemas import user_schemas
from app.schemas.responses_schemas import responses


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={**responses},
)


@router.post(
    "/create",
    dependencies=[Depends(users_create)],
    status_code=status.HTTP_201_CREATED,
    responses={201: {"model": schemas_config.GoodMessage}},
    summary="Create new User in the app",
)
async def create_user(
    request: user_schemas.UserCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """**Create new User**.

    Create new users in the application.

    - This Endpoint performs the operation of
     creating a new user in the application
     and storing it in the database.
    - Users can access when the role is assigned
     permission **create** to the module **users**.

    ***Important Note***
    - In case that you introduce a
     repeat email this not save in database.
    - To create a user, a role should be created.

    ***Parameters***:
    - Access Token

    **Request body parameter**:
     - user: **UserCreate** -> A UserCreate model with
      email, password and role

    *Return*:
    - **JSON Response** -> succesfull message
    - **status code** -> 201

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions().create_new_user(db, current_user, request)


@router.get(
    "/",
    dependencies=[Depends(users_read)],
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.ShowUsers,
    summary="Get All Users",
)
async def all_users(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None,
) -> JSONResponse:
    """**Get a list of Users**.

    Get a list of all users registered in the application

    - This Endpoint performs the operation of obtaining
     a list of users in the application, you can also paginate the records.
    - Users can access when the role is assigned
     permission **read** to the module **users**.

    **Parameters** :
    - Access Token

    **Query Parameters**:
    - ***start*** is a initial value from start to show (Optional)
    - ***limit*** is the end of the values to show (Optional)

    *Returns*
    - user: **ShowUser** -> A ShowUser model
     with: id (UUDI Format), email, status,
     created_on, role_id, role_name.
    - **status code** -> 200

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions().get_all_users(db, current_user, start, limit)


@router.get(
    "/{id}",
    dependencies=[Depends(users_read)],
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.ShowUser,
    summary="Get Specific User by id",
)
async def get_user(
    id: UUID, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """**Get One User**.

    Get a user in the application using your ID (UUID Format), as a filter.

    - This Endpoint performs the operation of obtaining a
    user of the application using the ID as a filter.
    - Users can access when the role is assigned
     permission **read** to the module **users**.

    **Parameters**:
    - Access Token

    **Path Parameter**:
    - User id -> (UUDI Format).

    *Return*:
    - user: **ShowUser** -> A ShowUser model
     with: id (UUDI Format), email, status, created_on,
     role_id (UUDI Format), role_name
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return UsersActions().get_one_user(db, id)


@router.put(
    "/{id}",
    dependencies=[Depends(users_update)],
    status_code=status.HTTP_202_ACCEPTED,
    responses={202: {"model": schemas_config.GoodMessage}},
    summary="Update User Information",
)
async def update_user(
    request: user_schemas.UpdateUser,
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """***Update User***.

    Update a user's information using your ID to select it.

    - This Endpoint performs the User Information Operation operation.
    - Choose the user by ID (UUID FORMAT).
    - The Email, Is_active and Search fields are optional,
     if the API is allowed to take the current value of those fields
    - The role_id field is mandatory.
     This means that the value to perform this operation must be indicated.
    - Users can access when the role is assigned
     to permission **update** to the module **users**.

    **Parameters**:
    - Access Token

    **Request body parameter**:
    - user: **UpdateUser** -> An User model with
     email (optinal), is_active (optinal),
     searches (optinal), role_id

    **Path Parameter**:
    - **User ID** -> (UUDI Format).

    *Return*:
    - **JSON Response** -> string message
    - **status code** -> 202

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions().update_user_info(db, id, request, current_user)


@router.patch(
    "/{id}/update/passwords",
    dependencies=[Depends(users_update)],
    status_code=status.HTTP_202_ACCEPTED,
    responses={202: {"model": schemas_config.GoodMessage}},
    summary="Update specific User password",
)
async def update_password(
    request: user_schemas.UpdatePass,
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """***Update Password***.

    Update a user's password using your ID to select it.

    - This Endpoint performs the operation of the password
     of a specific user.
    - Select the user for your ID (UUID FORMAT).
    - Confirm the new password checking the request
     with "new_password" and "password_confirmation"
     both fields are necessary.
    - Users can access when the role is assigned
     to permission **update** to the module **users**.

    **Parameters**:
    - Access Token

    **Request body parameter **:
    - user: **UpdatePass** -> An UpdatePass model
     with new_password, password_confirmation.

    **Path Parameter**:
    - **User ID** -> (UUDI Format).

    *Return*:
    - **JSON Response** -> string message
    - **status code** -> 202

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions().update_password_user(db, id, request, current_user)


@router.delete(
    "/{id}/delete/",
    dependencies=[Depends(users_delete)],
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete specific user using user id",
)
async def delete_user(
    id: UUID, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> Optional[JSONResponse]:
    """***Delete User***.

    Delete an User in the application by selecting it by ID.

    - This path operation delete users in the app by id from database.
    - Users can access when the role is assigned
     to permission **delete** to the module **users**.

    **Parameters**:
    - Access Token

    **Path Parameter**:
    - User ID -> (UUDI Format).

    *Return*:
    - **status code** -> 204

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions().delete_one_user(db, id, current_user)

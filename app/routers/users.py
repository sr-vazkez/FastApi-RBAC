from typing import Optional, Union
from uuid import UUID
from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi_another_jwt_auth import AuthJWT
from app.dependencies.data_conexion import get_db
from app.schemas import schemas_config
from app.internal.users import UsersActions
from app.dependencies.verify_user import require_user
from app.schemas import user_schemas
from app.schemas.responses_schemas import responses
from app.dependencies.permissions_policy import (
    users_create,
    users_read,
    users_update,
    users_delete
)

router = APIRouter(prefix="/users",
                   tags=["Users"],
                   responses={**responses},
                   dependencies=[Depends(require_user)]
                   )


@router.post("/create", dependencies=[Depends(users_create)],
             status_code=status.HTTP_201_CREATED,
             responses={201: {"model": schemas_config.GodMessage}},
             summary="Create new User in the app"
             )
def create_user(
    request: user_schemas.UserCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),

) -> JSONResponse:
    """
    **Create new User**

    - This path operation creates a new user in the app and save the infomation in the database.
    - **Just Admin Users** has access to this route.

    ***Important Note***
    - In case that you introduce a repeat email this not save in database.

    ***Parameters***:
    - Access Token
    - Request body parameter:
    - **user: UserCreate** -> A user model with email, password and role

    **Return**: 
    - **succesfull message** with **status code 200.** 

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions.create_new_user(db, current_user, request)


@router.get("/", dependencies=[Depends(users_read)],
            response_model=user_schemas.ShowUsers,
            summary="Get All Users",
            status_code=status.HTTP_200_OK,
            )
def all_users(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None
) -> JSONResponse:
    """
    **Get Users**

    - This path operation gets all users store in database
    - **Just Admin Users** has access to this route.

    **Parameters** :
    - Access Token
    - **Query Parameters**: 
        - ***start*** is a initial value from start to show
        - ***limit*** is the end of the values to show  

    *Request body parameter* :
    - **user: ShowUser** 

    *Returns* 
    - **users list** with:
    - id
    - email
    - status
    - role
    - date of register

    """
    Authorize.jwt_required()
    return UsersActions.get_all_users(db, start, limit)


@router.get("/{id}", dependencies=[Depends(users_read)],
            status_code=200,
            response_model=user_schemas.ShowUser,
            summary="Get Specific User by id",
            )
def get_user(
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """
    **Get User**

    - This path operation gets a one user
        by ID and show the infomation from the database
    - **Just Admin Users** has access to this route.

    ***Parameters***:

    - **Request body parameter**:
    - **user: ShowUser** -> A user model with: id, email,status,created_on,role id,role name,role created on
    - **Path Parameter**: 
        - User id. 

    Return 
    - **User model** with:
    - id 
    - email
    - status
    - created_on
    - role id
    - role name
    - role created on

    """
    Authorize.jwt_required()
    return UsersActions.get_one_user(db, id)


@router.put("/{id}", dependencies=[Depends(users_update)],
            status_code=status.HTTP_202_ACCEPTED,
            responses={202: {"model": schemas_config.GodMessage}},
            summary="Update User Information",
            )
def update_user(
    request: user_schemas.UpdateUser,
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """
    ***Update User*** 

    - This path operation update an user information in the app
    by id and save the infomation from the database.
    - You can edit all fields 
    - **Just Admin Users** has access to this route.

    **Parameters**:

    - Request body parameter:
    - **user: UpdateUser** -> An User model with id and updated email, status or role
    - ***Path Parameter*** : 
        - **User id**. 

    Return: 
    - **status code 202** and **string message.** 

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions.update_user_info(db, id, request, current_user)


@router.patch("/{id}/update/passwords", dependencies=[Depends(users_update)],
              summary="Update specific User password",
              status_code=status.HTTP_202_ACCEPTED,
              responses={202: {"model": schemas_config.GodMessage}}
              )
def update_password(
    request: user_schemas.UpdatePass,
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """
    ***Update Password***

    - This path operation update users password in the app by id in the database
    - Confirm the new password checking the request with "new_password" and "password_confirmation"
    - **Just Admin Users** has access to this route.

    **Parameters**:
    - Access Token
    - Request body parameter:
    - **user: UpdatePass** -> An User model with id and 
    - Path Parameter: User id (UUDI Format). 

    Return 
    - **status code 202** and **string message**

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions.update_password_user(db, id, request, current_user)


@router.delete("/{id}/delete/", dependencies=[Depends(users_delete)],
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete specific User using user id",
               response_class=Response,
               )
def delete_user(
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()

) -> Optional[JSONResponse]:
    """
    ***Delete User***

    - This path operation delete users in the app by id from database
    - **Just Admin Users** has access to this route.

    **Parameters**:
    - Access Token
    - Request path parameter: **user id**
    Return Just **CODE 204**

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions.delete_one_user(db, id, current_user)

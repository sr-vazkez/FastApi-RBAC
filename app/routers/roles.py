from typing import Optional, Union
from uuid import UUID


from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy.orm import Session


from app.dependencies.data_conexion import get_db
from app.dependencies.permissions_policy import (
    roles_create,
    roles_read,
    roles_update,
    roles_delete,
)
from app.internal.roles import RoleActions
from app.schemas import schemas_config, role_schemas
from app.schemas.responses_schemas import responses


router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    responses={**responses},
)


@router.post(
    "/create",
    dependencies=[Depends(roles_create)],
    status_code=status.HTTP_201_CREATED,
    responses={201: {"model": schemas_config.GoodMessage}},
    summary="Create new Role",
)
async def create_role(
    request: role_schemas.RoleCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """**Create new Role**.

    Create new roles in the application.

    - This endpoint creates a new role in the app and save
     the infomation in the database.
    - Users can access when the role is assigned
     to permission **create** to the module **roles**.

    ***Important Note***
    - In case that you introduce a repeat role this not save in database.

    ***Parameters***:
    - Access Token

    **Request body parameter**:
    - role: **RoleCreate** -> A RoleCreate model with
     name and description (Optional).

    *Return*:
    - **JSON Response** -> succesfull message
    - **status code** -> 201

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return RoleActions().create_new_role(db, request, current_user)


@router.get(
    "/",
    dependencies=[Depends(roles_read)],
    status_code=status.HTTP_200_OK,
    response_model=role_schemas.ShowRoles,
    summary="Get All Roles",
)
async def all_roles(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None,
) -> JSONResponse:
    """**Get a list of Roles**.

    Obtain a list of all the roles recorded in the application

    - This Endpoint performs the operation of obtaining a
     list of roles in the application, you can also paginate the records.
    - Users can access when the role is assigned
     permission **read** to the module **roles**.

    **Parameters** :
    - Access Token

    **Query Parameters**:
    - ***start*** is a initial value from start to show
    - ***limit*** is the end of the values to show

    *Returns*
    - role: **ShowRoles**  -> A ShowActions model
     with: id (UUDI Format), name, description.
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return RoleActions().get_all_roles(db, start, limit)


@router.get(
    "/{id}",
    dependencies=[Depends(roles_read)],
    status_code=status.HTTP_200_OK,
    responses={200: {"model": role_schemas.ShowRole}},
    response_model=role_schemas.ShowRole,
    summary="Get Specific Role by id",
)
async def show_role(
    id: UUID, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """**Get one Role**.

    This enpoint gets a role filtering by ID and
    show the information from the database.

    - Users can access when the role is assigned
     permission **read** to the module **roles**.

    ***Parameters***:
    - Access Token

    **Path Parameter**:
    - role id -> (UUDI Format).

    Return
    - role: **ShowRole** -> A ShowRole with id, name
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return RoleActions().get_one_role(db, id)


@router.put(
    "/{id}",
    dependencies=[Depends(roles_update)],
    status_code=status.HTTP_202_ACCEPTED,
    responses={202: {"model": schemas_config.GoodMessage}},
    summary="Update Role Information",
)
async def update_role(
    request: role_schemas.UpdateRole,
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """***Update Role***.

    Update the information of a role using your ID to select it.

    - This Endpoint performs the Role's Information Operation.
    - Name and description fields are optional
     This means that the API is left empty,
     it will take the current value of those fields.
    - Select the module for your ID (uuid format).
    - Users can access when the role is assigned
     permission **update** to the module **roles**.

    **Request body parameter**:
    - role: **UpdateRole** -> A UpdateModule model
     with: name (Optional), description (Optional).

    **Path Parameter** :
    - Role id -> (UUDI Format).

    *Return*:
    - **JSON Response** -> string message
    - **status code** -> 202

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return RoleActions().update_role_info(db, id, request, current_user)


@router.delete(
    "/{id}/delete/",
    dependencies=[Depends(roles_delete)],
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete specific Role using user id",
)
async def delete_role(
    id: UUID, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> Optional[JSONResponse]:
    """***Delete Role***.

    - This path operation delete roles in the app by id from database
    - Users can access when the role is assigned
     permission **delete** in the module **roles**.

    ***IMPORTANT***
    - To eliminate a role first, users associated
     with said role must be eliminated.

    **Parameters**:
    - Access Token

    **Path Parameter**:
    - Role ID -> (UUDI Format).

    *Return*
    - **status code** -> 204

    """
    Authorize.jwt_required()
    return RoleActions().delete_one_role(db, id)


@router.get(
    "/{id}/users",
    dependencies=[Depends(roles_read)],
    status_code=status.HTTP_200_OK,
    response_model=role_schemas.ShowRoleWithUsers,
    summary="Show a role with the users assigned",
)
async def show_role_with_users(
    id: UUID,
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None,
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """***Show a role with the users***.

    Obtain the users assigned to a role selected the role for their id.

    - This Endpoint does is ask for the id of a role to show you
    To all users who have assigned that role.
    - This Endpoint can also paginate these results.
    - Users can access when the role is assigned
     permission **read** to the module **roles**.

    ***Parameters***:
    - Access Token

    **Path Parameter**:
    - Role id -> (UUID Format).

    **Query Parameters**:
    - ***start*** is a initial value from start to show
    - ***limit*** is the end of the values to show

    *Return*
    - role: **ShowRoleWithUsers** -> A ShowRoleWithUsers model
     with: id (UUID Format), name, description, user_id (UUID Format),
     user_email, user_is_active, user_searches
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return RoleActions().show_role_with_users(db, id, start, limit)


@router.get(
    "/{id}/permissions",
    dependencies=[Depends(roles_read)],
    status_code=status.HTTP_200_OK,
    response_model=role_schemas.ShowRoleWithPermission,
    summary="Get Specific Role by id and return permissions",
)
async def permission_query(
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """**Get one Role with permissions**.

    Get a role with your permissions assigned in
     the application using your ID as a filter.

    - This Endpoint performs the operation of obtaining
     the information of an application action
     using the ID (UUDI Format), as a filter.
    - Users can access when the role is assigned
     permission **read** to the module **roles**.

    ***Parameters***:
    - Access Token

    **Path Parameter**:
    - role id -> (UUDI Format).

    *Return*:
    - role: **ShowRole** -> A ShowRole model
     with: id, name, description,
     permissions (Optional List of Permissions).
    - **status code** -> 200


    """
    Authorize.jwt_required()
    return RoleActions().show_actions_and_modules(db, id)

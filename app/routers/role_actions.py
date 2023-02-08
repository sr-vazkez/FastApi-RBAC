from typing import Optional, Union
from uuid import UUID


from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy.orm import Session


from app.dependencies.data_conexion import get_db
from app.dependencies.permissions_policy import (
    permissions_create,
    permissions_read,
    permissions_update,
    permissions_delete,
)
from app.internal.role_action import RoleActions
from app.schemas import schemas_config
from app.schemas import role_actions_schemas
from app.schemas.responses_schemas import responses


router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
    responses={**responses},
)


@router.get(
    "/",
    dependencies=[Depends(permissions_read)],
    status_code=status.HTTP_200_OK,
    response_model=role_actions_schemas.ShowRoleActions,
    summary="Show all actions assigned",
)
async def show_all(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    start: Union[int, None] = None,
    limit: Union[int, None] = None,
) -> JSONResponse:
    """**Get a list Role Actions**.

    Obtain a list of all the actions of a role recorded in the application

    - This Endpoint performs the operation of obtaining a
     list of actions assigned to a role in the application.
    - Users can access when the role is assigned
     permission **read** to the module **permissions**.

    **Parameters** :
    - Access Token

    **Query Parameters**:
    - ***start*** is a initial value from start to show
    - ***limit*** is the end of the values to show

    *Return*
    - Role-Actions: **ShowRoleActions** -> A ShowRoleActions model
     with: id (UUDI Format), actions_id (UUDI Format), action_name,
     role_id (UUDI Format),role_name, role_name
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return RoleActions().show_all_actions_assigned(db, start, limit)


@router.get(
    "/{id}",
    dependencies=[Depends(permissions_read)],
    status_code=status.HTTP_200_OK,
    response_model=role_actions_schemas.ShowRoleAction,
    summary="Show one register filter by ID",
)
async def show_one(
    id: UUID, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """**Get one Role Action registry**.

    Get an Action Role in the application using your ID as a filter.

    - This path operation gets one registry filtering by ID an show
     the information from the database.
    - Users can access when the role is assigned
     permission **read** to the module **permissions**.

    **Parameters**:
    - Access Token

    **Path Parameter**:
    - Role-Action id -> (UUDI Format).

    *Return*
    - Role-Actions: **ShowRoleAction** -> A ShowRoleAction model
     with: id (UUDI Format), actions_id (UUDI Format), action_name,
     role_id (UUDI Format),role_name, role_name
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return RoleActions().show_one_role_action(db, id)


@router.post(
    "/assing/actions",
    dependencies=[Depends(permissions_create)],
    status_code=status.HTTP_201_CREATED,
    responses={201: {"model": schemas_config.GoodMessage}},
    summary="Assign action to role",
)
async def assing_actions_to_role(
    request: role_actions_schemas.assigned_action,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """**Assing Action to a Role**.

    Assign an action to a role.

    - This path operation assing a new action in a role and
     save the infomation in the database.
    - Users can access when the role is assigned
     to permission **create** to the module **permissions**.

    ***Important Note***
    - In case you repeat the allocation,
     it would be notified that it had already been created
    - The description field is an optional value
     so there is no problem when sending it empty

    ***Parameters***:
    - Access Token

    **Request body parameter**:
    - role-action: **assigned_action** -> A role model with
    role_id (UUDI Format), actions_id (UUDI Format) and description (Optional).

    *Return*:
    - **JSON Response** -> succesfull message
    - **status code** -> 201

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return RoleActions().assing_role_and_actions(db, request, current_user)


@router.put(
    "/{id}",
    dependencies=[Depends(permissions_update)],
    status_code=status.HTTP_202_ACCEPTED,
    responses={202: {"model": schemas_config.GoodMessage}},
    summary="Update description in permission",
)
async def update_description(
    id: UUID,
    request: role_actions_schemas.update_assigned_action_desc,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """**Update description in permission**.

    Update the description of an Action Role using your ID to select it.

    - This path operation update description and save the infomation in the database.
    - Select the Role Action for your ID (UUDI Format).
    - Users can access when the role is assigned
     to permission **update** to the module **permissions**.

    ***Parameters***:
    - Access Token

    **Request body parameter**:
    - role-action:**update_assigned_action_desc**  -> description (Optional).

    *Return*:
    - **JSON Response** -> string message
    - **status code** -> 202

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return RoleActions().update_description(db, id, request, current_user)


@router.delete(
    "/{id}/delete/",
    dependencies=[Depends(permissions_delete)],
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete a action to a role",
)
async def unassing_actions_to_role(
    id: UUID, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> Optional[JSONResponse]:
    """**Delete actions to role**.

    Delete an action to a role.

    - This path operation what it does is unassign acction from a role
    - Users can access when the role is assigned
     to permission **delete** to the module **permissios**.

    **Parameters**:
    - Access Token

    **Path parameter**:
    - Permission ID -> (UUDI Format).

    *Return*
    - **status code** -> 204

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return RoleActions().deleted_assing_role_and_actions(db, id, current_user)

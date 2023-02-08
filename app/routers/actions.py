from typing import Optional, Union
from uuid import UUID

from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.dependencies.data_conexion import get_db
from app.dependencies.permissions_policy import (
    actions_create,
    actions_read,
    actions_update,
    actions_delete,
)
from app.internal.actions import ActionsOperations
from app.schemas import action_schemas
from app.schemas import schemas_config
from app.schemas.responses_schemas import responses


router = APIRouter(
    prefix="/actions",
    tags=["Actions"],
    responses={**responses},
)


@router.post(
    "/create",
    dependencies=[Depends(actions_create)],
    status_code=status.HTTP_201_CREATED,
    responses={201: {"model": schemas_config.GoodMessage}},
    summary="Create new action in the app",
)
async def create_action(
    request: action_schemas.ActionCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """**Create Action Role**.

    Create new actions in the application.

    - This Endpoint performs the operation of creating a new action in
     the application and storing it in the database.
    - Users can access when the role is assigned to
     permission **create** to the Module **actions**.

    ***Important Note***
    - To create an action, a module should be created.
    - In case that you introduce a repeat action in a module
     this not save in database.
    - In case that you introduce invalid module id this
     return a HTTP ERROR

    ***Parameters***:
    - Access Token

    **Request body parameter**:
    - actions: **ActionCreate** -> An ActionCreate model with action_name,
     value and module_id (UUDI Format).

    **Return**:
    - **JSON Response** -> succesfull message
    - **status code** -> 201

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return ActionsOperations().create_new_action(db, current_user, request)


@router.get(
    "/",
    dependencies=[Depends(actions_read)],
    status_code=status.HTTP_200_OK,
    response_model=action_schemas.ShowActions,
    summary="Get All Actions",
)
async def all_actions(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None,
) -> JSONResponse:
    """**Get a list of Actions**.

    Obtain a list of all the actions recorded in the application

    - This Endpoint performs the operation of obtaining a list of
     shares in the application, you can also paginate the records.
    - Users can access when the role is assigned to permission
     **read** to the module **actions**.

    **Parameters** :
    - Access Token

    **Query Parameters**:
    - ***start*** is a initial value from start to show
    - ***limit*** is the end of the values to show


    *Returns*
    - action: **ShowActions** -> A ShowActions model with: id (UUDI Format),
     action_name, description, is_active, module_id (UUDI Format).
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return ActionsOperations().get_all_actions(db, start, limit)


@router.get(
    "/{id}",
    dependencies=[Depends(actions_read)],
    status_code=status.HTTP_200_OK,
    response_model=action_schemas.ShowAction,
    summary="Get Specific Action by id",
)
async def get_action(
    id: UUID, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """**Get One Action**.

    Get an action in the application using your ID as a filter.

    - This Endpoint performs the operation of obtaining the information
     of an application action using the ID (UUDI format), as a filter.
    - Users can access when the role is assigned to
     permission **read** to the module **actions**.

    **Parameters**:
    - Access Token

    **Path Parameter**:
    - Action id -> (UUDI Format).

    *Return*
    - action: **ShowActions** -> A ShowActions model with: id (UUDI Format),
     action_name, description, is_active, module_id (UUDI Format).
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return ActionsOperations().get_one_action(db, id)


@router.put(
    "/{id}",
    dependencies=[Depends(actions_update)],
    status_code=status.HTTP_202_ACCEPTED,
    responses={202: {"model": schemas_config.GoodMessage}},
    summary="Update Action Information",
)
async def update_action(
    request: action_schemas.UpdateAction,
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """***Update Action***.

    Update the information of an action using your ID to select it.

    - This Endpoint performs the operation of the action of the action.
    - Select the action for your ID (UUDI Format).
    - The action_name and description fields are optional.
    if the API is left empty, it will take the current value of those fields.
    - The is_Active field is mandatory.
     This means that the value to perform this operation must be indicated.
    - Users can access when the role is assigned
     to permission **update** to the module **actions**.

    **Parameters**:
    - Access Token

    **Request body parameter**:
    - action: **UpdateAction** -> An UpdateAction model with action_name (Optional),
     is_active (Obligatory) and description (Optional).

    **Path Parameter**:
    - Action id -> (UUDI Format).

    Return:
    - **JSON Response** -> string message
    - **status code** -> 202

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return ActionsOperations().update_action_info(db, id, request, current_user)


@router.delete(
    "/{id}/delete/",
    dependencies=[Depends(actions_delete)],
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete specific Action using user id",
)
async def delete_action(
    id: UUID, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> Optional[JSONResponse]:
    """***Delete Action***.

    Delete an action in the application by selecting it by its id.

    - This path operation delete actions in the app by id from database.
    - Users can access when the role is assigned
     to permission **delete** to the module **actions**.

    **Parameters**:
    - Access Token

    **Path Parameter**:
    - Actions ID -> (UUDI Format).

    Return
    - **status code** -> 204

    """
    Authorize.jwt_required()
    return ActionsOperations().delete_one_action(db, id)

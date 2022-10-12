from uuid import UUID
from typing import Optional, Union

from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi_another_jwt_auth import AuthJWT

from app.dependencies.data_conexion import get_db
from app.dependencies.verify_user import require_user
from app.schemas import schemas_config
from app.internal.actions import ActionsOperations
from app.schemas import action_schemas
from app.schemas.action_schemas import ActionCreate, UpdateAction
from app.schemas.responses_schemas import responses
from app.dependencies.permissions_policy import (
    actions_create,
    actions_read,
    actions_update,
    actions_delete
)

router = APIRouter(prefix="/actions",
    tags=["Actions"],
    responses={**responses},
    dependencies=[Depends(require_user)]
)


@router.post("/create",dependencies=[Depends(actions_create)],
             status_code=status.HTTP_201_CREATED,
             responses={201: {"model": schemas_config.GodMessage}},
             summary="Create new action in the app",

             )
def create_action(
    request: ActionCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()

) -> JSONResponse:
    """
    **Create Action Role**

    - This path operation creates a new action in the app and save the infomation in the database.
    - **Just Admin Users** has access to this route.

    ***Important Note***
    - In case that you introduce a repeat action in a module this not save in database.
    - In case that you introduce invalid module id this return a HTTP ERROR

    ***Parameters***:
    - Access Token
    - Request body parameter:
    - **actions: ActionCreate** -> Action model with action_name, value and module_id

    **Return**: 
    - **succesfull message** with **status code 200.** 
    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return ActionsOperations.create_new_action(db, current_user, request)


@router.get("/",dependencies=[Depends(actions_read)],
            response_model=action_schemas.ShowActions,
            summary="Get All Actions",
            status_code=status.HTTP_200_OK
            )
def all_actions(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None

) -> JSONResponse:
    """
    **Get Actions**

    - This path operation gets all actions store in database
    - **Just Admin Users** has access to this route.

    **Parameters** :
    - Access Token
    - **Query Parameters**: 
        - ***start*** is a initial value from start to show
        - ***limit*** is the end of the values to show  

    *Request body parameter* :
    - **action: ShowActions** 

    *Returns* 
    - **actions list** with:
    - id
    - action_name
    - value
    - created_on
    - module_id
    - module_name
    - module_created_on

    """
    Authorize.jwt_required()
    return ActionsOperations.get_all_actions(db, start, limit)


@router.get("/{id}",dependencies=[Depends(actions_read)],
            status_code=200,
            response_model=action_schemas.ShowAction,
            summary="Get Specific Action by id"
            )
def get_action(
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """
    **Get Action**

    - This path operation gets a role filtering by ID and 
    show the information from the database.
    - **Just Admin Users** has access to this route.

    ***Parameters***:

    - **Request body parameter**:
    - **action: ShowAction** -> Action model with id, action_name, value, created_on, module_id, module_name, module_created_on.
    - **Path Parameter**: 
        - Action id. 

    Return 
    - **Action model** with:
    - id
    - action_name
    - value
    - created_on
    - module_id
    - module_name
    - module_created_on

    """
    Authorize.jwt_required()
    return ActionsOperations.get_one_action(db, id)


@router.put("/{id}/module/",dependencies=[Depends(actions_update)],
            status_code=status.HTTP_202_ACCEPTED,
            responses={202: {"model": schemas_config.GodMessage}},
            summary="Update Action Information"
            )
def update_action(
    request: UpdateAction,
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """
    ***Update Action*** 

    - This path operation update an action information in the app
    by id and save the infomation from the database.
    - You can edit all fields 
    - **Just Admin Users** has access to this route.

    **Parameters**:

    - Request body parameter:
    - **action: UpdateAction** -> An Action model with id and updated email, status or role
    - ***Path Parameter*** : 
        - **Action id**. 

    Return: 
    - **status code 202** and **string message.** 
    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return ActionsOperations.update_action_info(db, id,request, current_user)


@router.delete("/{id}/delete/",dependencies=[Depends(actions_delete)],
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete specific Action using user id",
               response_class=Response
               )
def delete_action(
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> Optional[JSONResponse]:
    """
    ***Delete Action***

    - This path operation delete users in the app by id from database
    - **Just Admin Users** has access to this route.

    **Parameters**:
    - Access Token
    - Request path parameter: **user id**
    Return Just **CODE 204**
    """
    Authorize.jwt_required()
    return ActionsOperations.delete_one_action(db, id)

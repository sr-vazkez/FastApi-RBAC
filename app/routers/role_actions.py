from typing import Optional, Union
from uuid import UUID


from fastapi import APIRouter, status, Depends, Response
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


from app.dependencies.data_conexion import get_db
from app.dependencies.verify_user import require_user
from app.internal.role_action import RoleActions
from app.schemas import role_actions_schemas
from app.schemas.responses_schemas import responses
from app.dependencies.permissions_policy import (
    permissions_create,
    permissions_update,
    permissions_delete,
    permissions_read
)

router = APIRouter(prefix="/permissions",
    tags=["Permissions"],
    responses={**responses},
    dependencies=[Depends(require_user)]
)

@router.get('/',dependencies=[Depends(permissions_read)],
    response_model = role_actions_schemas.ShowRoleActions,
    summary="Show all actions assigned",
    status_code=status.HTTP_200_OK
)
def show_all(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    start: Union[int, None] = None,
    limit: Union[int, None] = None
) -> JSONResponse:
    """
    **Get Role Actions Registries**

    - This path operation gets all Actions assigned a Role store in database
    - **Just Admin Users** has access to this route.

    **Parameters** :
    - Access Token
    - **Query Parameters**: 
        - ***start*** is a initial value from start to show
        - ***limit*** is the end of the values to show  

    *Request body parameter* :
    - **role-actions: ShowRoleActionsr** 

    *Returns* 
    - **users list** with:
    - id
    - actions_id
    - role_id
    - created_on

    """   
    Authorize.jwt_required()
    return RoleActions.show_all_actions_assigned(db, start, limit)


@router.get('/{id}',dependencies=[Depends(permissions_read)],
    response_model = role_actions_schemas.ShowRoleAction,
    summary="Show one register filter by ID"
)
def show_one(
    id: UUID,
    db:Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """**Get one Role Action registry**

    - This path operation gets one registry filtering by ID an show the information from the database.
    - **Just Admin Users** has access to this route.

    ***Parameters***:

    - **Request body parameter**:
    - **Role-Actions: ShowRoleAction** -> A Role-Acction model with: id, actions_id, role_id, created_on
    - **Path Parameter**: 
        - Role-Action id. 

    Return
    - **Role-Action model** with:
    - id
    - actions_id
    - role_id
    - create_on

    """
    Authorize.jwt_required()
    return RoleActions.show_one_role_action(db, id)

@router.post('/assing/actions',dependencies=[Depends(permissions_create)],
            summary="Assign actions to role",
)
def assing_actions_to_role(
    request: role_actions_schemas.assigned_action,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """**Assing Actions to a Role**
    
    - This path operation assing a new action in a role and save the infomation in the database.
    - **Just Admin Users** has access to this route.

    ***Important Note***
    - In case you repeat the allocation, it would be notified that it had already been created

    ***Parameters***:
    - Access Token
    - Request body parameter:
    - **role-action:assigned_action** -> A role model with role_id and actions_id.
    
    **Return**: 
    - **succesfull message** with **status code 200.** 

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return RoleActions.assing_role_and_actions(db, request, current_user)

@router.put('/{id}', dependencies=[Depends(permissions_update)],
    summary='Update description in a permission'
)
def update_description(
    request: role_actions_schemas.update_assigned_action_desc,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()

) -> JSONResponse:
    """
    Este endpoint lo que hace es actualizar la  
    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return 'ok'

@router.delete('/{id}/',dependencies=[Depends(permissions_delete)],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unassing a action to a role",
    response_class=Response
)
def unassing_actions_to_role(
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> Optional[JSONResponse]:
    """
    **Unassing actions to role**

    - This path operation what it does is unassign acction from a role
    - **Admins and Operators** has access for this route

    ***Parameters*** :

    - Access Token

    - **Path parameter**:
        - **id** (int): _server id_.
        - **people_id** (int): _people_id_.

    - **Returns**:
        - **status code 204**  
    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return RoleActions.deleted_assing_role_and_actions(db, id, current_user)


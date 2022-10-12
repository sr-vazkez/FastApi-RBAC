from typing import Union
from uuid import UUID
from fastapi import APIRouter,status, Depends, Response
from sqlalchemy.orm import Session
from fastapi_another_jwt_auth import AuthJWT
from app.dependencies.data_conexion import get_db
from app.dependencies.verify_user import require_user
from app.schemas import schemas_config
from app.internal.roles import RoleActions
from app.schemas import role_schemas
from app.schemas.responses_schemas import responses
from app.dependencies.permissions_policy import (
    roles_create,
    roles_read,
    roles_update,
    roles_delete
)


router = APIRouter(prefix="/roles",
    tags=["Roles"],
    responses={**responses},
    dependencies=[Depends(require_user)]
)


@router.post("/create", dependencies=[Depends(roles_create)],
             status_code=status.HTTP_201_CREATED,
             responses={201: {"model": schemas_config.GodMessage}},
             summary="Create new Role",
             )
def create_role(
    request: role_schemas.RoleCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
    **Create new Role**

    - This path operation creates a new role in the app and save the infomation in the database.
    - **Just Admin Users** has access to this route.
    
    ***Important Note***
    - In case that you introduce a repeat role this not save in database.
    
    ***Parameters***:
    - Access Token
    - Request body parameter:
    - **role:RoleCreate** -> A role model with name.
    
    **Return**: 
    - **succesfull message** with **status code 200.** 

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return RoleActions.create_new_role(db, request, current_user)
    

@router.get("/", dependencies=[Depends(roles_read)],
            response_model=role_schemas.ShowRoles,
            summary="Get All Roles",
            status_code=status.HTTP_200_OK
            )
def all_roles(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None
):
    """
    **Get Roles**
       
     - This path operation gets all roles store in database
    - **Just Admin Users** has access to this route.

    **Parameters** :
    - Access Token
    - **Query Parameters**: 
        - ***start*** is a initial value from start to show
        - ***limit*** is the end of the values to show  

    *Request body parameter* :
    - **role: ShowRoles** 

    *Returns* 
    - **roles list** with:
    - id
    - name
    - date of register

    """
    Authorize.jwt_required()
    return RoleActions.get_all_roles(db, start, limit)


@router.get("/{id}", dependencies=[Depends(roles_read)],
            status_code=200,
            response_model=role_schemas.ShowRole,
            summary="Get Specific Role by id"
            )
def show_role(
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
    **Get one Role**
    
    - This path operation gets a role filtering by ID and 
    show the information from the database.
    - **Just Admin Users** has access to this route.
    
    ***Parameters***:

    - **Request body parameter**:
    - **role: ShowRole** -> A role model with: id, name,created_on
    - **Path Parameter**: 
        - role id. 

    Return
    - **Role model** with:
    - id
    - name
    - create_on

    """
    Authorize.jwt_required()
    return RoleActions.get_one_role(db, id)


@router.put("/{id}", dependencies=[Depends(roles_update)],
            status_code=status.HTTP_202_ACCEPTED,
            responses={202: {"model": schemas_config.GodMessage}},
            summary="Update Role Information"
            )
def update_role(
    request: role_schemas.UpdateRole,
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()

):
    """
    ***Update Role*** 
    
    - This path operation update an role information in the app
    by id and save the infomation from the database.
    - **Just Admin Users** has access to this route.

    - Request body parameter:
    - **role: UpdateRole** -> A Role model with id and updated name.
    - ***Path Parameter*** : 
        - **Role id**. 

    Return: 
    - **status code 202** and **string message.** 

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return RoleActions.update_role_info(db, id, request, current_user)


@router.delete("/{id}/delete/",dependencies=[Depends(roles_delete)],
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete specific Role using user id",
               response_class=Response

               )
def delete_role(
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()

):
    """
    ***Delete Role***
    
    - This path operation delete roles in the app by id from database
    - **Just Admin Users** has access to this route.

    **Parameters**:

    - Access Token
    - Request path parameter: **role id**

    Return Just **CODE 204**

    """
    Authorize.jwt_required()
    return RoleActions.delete_one_role(db, id)


@router.get("/{id}/users",dependencies=[Depends(roles_read)],
                status_code=200,
                response_model=role_schemas.ShowRoleWithUsers,
                summary="Show a role with the users assigned"
)
def show_role_with_users(
    id: UUID,
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None,
    Authorize: AuthJWT = Depends()
):
    """
    ***Show a role with the users*** 
        
    - This path operation lo que hace es pedir el id de un rol para mostrarte 
    a todos los usuarios que tengan asignados ese rol. 

    - **Just Admin Users** has access to this route.

    ***Parameters***:

    - **Request body parameter**:
    - **user: ShowRoleWithUsers** -> A user model with: id, name, created_on, 
    user_id, user_email, user_status, user_created_on,

    - **Path Parameter**: 
        - Role id. 
    Return 
    - **Role Model** with:
    - Role and User information

    """
    Authorize.jwt_required()
    return RoleActions.show_role_with_users(db,id,start,limit)


@router.get('/{role_id}/permissions',dependencies=[Depends(roles_read)],
            status_code=status.HTTP_200_OK
)
def permission_query(
    id: UUID,    
    db:Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    start: Union[int, None] = None,
    limit: Union[int, None] = None

):
    """Esta funcion lo que hace es buscar por el id del role nos regresa
    las acciones y al modulo al que pertenecen
    """
    Authorize.jwt_required()    
    return RoleActions.show_actions_and_modules(db, id, start, limit)


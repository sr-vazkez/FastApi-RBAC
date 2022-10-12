from typing import Optional, Union
from uuid import UUID
from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi_another_jwt_auth import AuthJWT
from app.dependencies.data_conexion import get_db
from app.dependencies.verify_user import require_user
from app.schemas import schemas_config
from app.internal.module import ModuleActions
from app.schemas import module_schemas
from app.schemas.responses_schemas import responses
from app.dependencies.permissions_policy import (
    modules_create,
    modules_read,
    modules_update,
    modules_delete
)


router = APIRouter(prefix="/modules",
    tags=["Modules"],
    responses={**responses},
    dependencies=[Depends(require_user)]
)


@router.post("/create",dependencies=[Depends(modules_create)],
             status_code=status.HTTP_201_CREATED,
             responses={201: {"model": schemas_config.GodMessage}},
             summary="Create new Module",

             )
def create_module(
    request: module_schemas.ModuleCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()

) -> JSONResponse:
    """
    **Create new Module**

    - This path operation creates a new module in the app and save the infomation in the database.
    - **Just Admin Users** has access to this route.

    ***Important Note***
    - In case that you introduce a repeat module this not save in database.

    ***Parameters***:
    - Access Token
    - Request body parameter:
    - **module:ModuleCreate** -> A module model with name.

    **Return**: 
    - **succesfull message** with **status code 200.** 

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return ModuleActions.create_module(db, request, current_user)


@router.get("/",dependencies=[Depends(modules_read)],
            response_model=module_schemas.ShowModules,
            summary="Get All Modules",
            status_code=status.HTTP_200_OK
            )
def all_modules(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None

) -> JSONResponse:
    """
    **Get Modules**

     - This path operation gets all Modules store in database
    - **Just Admin Users** has access to this route.

    **Parameters** :
    - Access Token
    - **Query Parameters**: 
        - ***start*** is a initial value from start to show
        - ***limit*** is the end of the values to show  

    *Request body parameter* :
    - **module: ShowModules** 

    *Returns* 
    - **module list** with:
    - id
    - name
    - date of register

    """

    Authorize.jwt_required()
    return ModuleActions.get_all_modules(db, start, limit)


@router.get("/{id}",dependencies=[Depends(modules_read)],
            status_code=200,
            response_model=module_schemas.ShowModule,
            summary="Get Specific Module by id"
            )
def get_module(
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()

) -> JSONResponse:
    """
    **Get one Module**

    - This path operation gets a module filtering by ID and 
    show the information from the database.
    - **Just Admin Users** has access to this route.

    ***Parameters***:

    - **Request body parameter**:
    - **module: ShowModule** -> A Module model with: id, name,created_on
    - **Path Parameter**: 
        - module id. 

    Return
    - **Module model** with:
    - id
    - name
    - create_on

    """
    Authorize.jwt_required()
    return ModuleActions.get_one_module(db, id)


@router.put("/{id}",dependencies=[Depends(modules_update)],
            status_code=status.HTTP_202_ACCEPTED,
            responses={202: {"model": schemas_config.GodMessage}},
            summary="Update Module Information"
            )
def update_user(
    request: module_schemas.UpdateModule,
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()

) -> JSONResponse:
    """
    ***Update Module*** 

    - This path operation update an module information in the app
    by id and save the infomation from the database.
    - **Just Admin Users** has access to this route.

    - Request body parameter:
    - **module: UpdateModule** -> A Module model with id and updated name.
    - ***Path Parameter*** : 
        - **Module id**. 

    Return: 
    - **status code 202** and **string message.** 

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return ModuleActions.update_module_info(db, id, request, current_user)


@router.delete("/{id}/delete/",dependencies=[Depends(modules_delete)],
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete specific Module using user id",
               response_class=Response
               )
def delete_user(
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> Optional[JSONResponse]:
    """
    ***Delete Module***

    - This path operation delete module in the app by id from database
    - **Just Admin Users** has access to this route.

    **Parameters**:

    - Access Token
    - Request path parameter: **module id**

    Return Just **CODE 204**


    """

    Authorize.jwt_required()
    return ModuleActions.deleted_one_module(db, id)


@router.get("/{id}/actions",dependencies=[Depends(modules_read)],
                status_code=200,
                response_model=module_schemas.ShowModuleWithActions,
                summary="Show a module with the actions assigned"
)
def show_module_with_actions(
    id: UUID,
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None,
    Authorize: AuthJWT = Depends()

) -> JSONResponse:
    """
    ***Show actions assigned to a module *** 
        
    - this Path Operation Looks For Id Of The Module And Returns Its Assigned Actions. 

    - **Just Admin Users** has access to this route.

    ***Parameters***:

    - **Request body parameter**:
    - **module: ShowModuleWithActions** -> A module model with: id, name, created_on, action_id, action_name, action_value, action_created_on

    - **Path Parameter**: 
        - Module id. 
    Return 
    - **Module Model** with:
        - Module and Action information

    """
    Authorize.jwt_required()
    return ModuleActions.show_module_with_action(db,id,start,limit)
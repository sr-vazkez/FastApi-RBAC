from typing import Optional, Union
from uuid import UUID


from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy.orm import Session


from app.dependencies.data_conexion import get_db
from app.dependencies.permissions_policy import (
    modules_create,
    modules_read,
    modules_update,
    modules_delete,
)
from app.internal.module import ModuleActions
from app.schemas import schemas_config, module_schemas
from app.schemas.responses_schemas import responses


router = APIRouter(
    prefix="/modules",
    tags=["Modules"],
    responses={**responses},
)


@router.post(
    "/create",
    dependencies=[Depends(modules_create)],
    status_code=status.HTTP_201_CREATED,
    responses={201: {"model": schemas_config.GoodMessage}},
    summary="Create new Module",
)
async def create_module(
    request: module_schemas.ModuleCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """**Create Module**.

    Create new modules in the application.

    - This Endpoint performs the operation of creating a
     new module in the application and storing it in the database.
    - Users can access when the role is assigned
     to permission **create** to the module **modules**.

    ***Important Note***
    - In case that you introduce a repeat module this not save in database.

    ***Parameters***:
    - Access Token

    **Request body parameter**:
    - module: **ModuleCreate** -> A ModuleCreate model
     with name and description.

    *Return*:
    - **JSON Response** -> succesfull message
    - **status code** -> 201

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return ModuleActions().create_module(db, request, current_user)


@router.get(
    "/",
    dependencies=[Depends(modules_read)],
    status_code=status.HTTP_200_OK,
    response_model=module_schemas.ShowModules,
    summary="Get All Modules",
)
async def all_modules(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None,
) -> JSONResponse:
    """**Get a list of Modules**.

    Obtain a list of all the modules recorded in the application

    - This Endpoint performs the operation of obtaining a list
     of modules in the application, you can also paginate the records.
    - Users can access when the role is assigned
     to permission **read** to the module **modules**.

    **Parameters** :
    - Access Token

    **Query Parameters**:
    - ***start*** is a initial value from start to show
    - ***limit*** is the end of the values to show

    *Returns*
    - module: **ShowModules**  -> A ShowActions model
     with: id (UUDI Format), name, description.
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return ModuleActions().get_all_modules(db, start, limit)


@router.get(
    "/{id}",
    dependencies=[Depends(modules_read)],
    status_code=status.HTTP_200_OK,
    response_model=module_schemas.ShowModule,
    summary="Get Specific Module by id",
)
async def get_module(
    id: UUID, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """**Get one Module**.

    Get a module in the application using your ID as a filter.

    - This Endpoint performs the operation of obtaining the information
     of an application action using the ID (UUDI Format), as a filter.
    - Users can access when the role is assigned
     to permission **read** to the module **modules**.

    ***Parameters***:
    - Access Token

    **Path Parameter**:
    - Module id -> (UUDI Format).

    *Return*
    - module: **ShowModule** -> A ShowModule model
     with: id (UUDI Format), name, description
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return ModuleActions().get_one_module(db, id)


@router.put(
    "/{id}",
    dependencies=[Depends(modules_update)],
    status_code=status.HTTP_202_ACCEPTED,
    responses={202: {"model": schemas_config.GoodMessage}},
    summary="Update Module Information",
)
async def update_module(
    request: module_schemas.UpdateModule,
    id: UUID,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """***Update Module***.

    Update the information of a module using your ID to select it.

    - This Endpoint performs the update information information.
    - Name and description fields are optional This means that the API
     is left empty, it will take the current value of those fields.
    - Select the module for your ID (UUDI Format).
    - Users can access when the role is assigned
     to permission **update** to the module **modules**.

    **Request body parameter**:
    - module: **UpdateModule** -> A UpdateModule model
     with: name (Optional), description (Optional).

    **Path Parameter** :
    - Module id -> (UUDI Format).

    *Return*:
    - **JSON Response** -> string message
    - **status code** -> 202

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return ModuleActions().update_module_info(db, id, request, current_user)


@router.delete(
    "/{id}/delete/",
    dependencies=[Depends(modules_delete)],
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete specific Module using user id",
)
async def delete_module(
    id: UUID, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> Optional[JSONResponse]:
    """***Delete Module***.

    Delete a module in the application by selecting it by its id.

    - This path operation delete module in the app by id from database
    - Users can access when the role is assigned
     to permission **delete** to module **modules**.

    ***IMPORTANT***
    - To delete a module, the actions associated with said module
     must be eliminated.

    **Parameters**:
    - Access Token

    **Path Parameter**:
    - Module ID -> (UUDI Format).

    *Return*
    - **status code** -> 204

    """
    Authorize.jwt_required()
    return ModuleActions().deleted_one_module(db, id)


@router.get(
    "/{id}/actions",
    dependencies=[Depends(modules_read)],
    status_code=status.HTTP_200_OK,
    response_model=module_schemas.ShowModuleWithActions,
    summary="Show a module with the actions assigned",
)
async def show_module_with_actions(
    id: UUID,
    db: Session = Depends(get_db),
    start: Union[int, None] = None,
    limit: Union[int, None] = None,
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """***Show actions assigned to a module ***.

    Obtain the actions assigned to a selected module for your ID.

    - This endpoint Looks For Id Of The Module And Returns
     Its Assigned Actions.
    - This endpoint can also paginate these results.
    - Users can access when the role is assigned
     to permission **read** to the module **modules**.

    ***Parameters***:
    - Access Token

    **Path Parameter**:
    - Module id -> (UUID Format).

    **Query Parameters**:
    - ***start*** is a initial value from start to show
    - ***limit*** is the end of the values to show

    *Return*
    - module: **ShowModuleWithActions** -> A module model
     with: id (UUID Format), name, action_id, action_name, action_is_active
    - **status code** -> 200

    """
    Authorize.jwt_required()
    return ModuleActions().show_module_with_action(db, id, start, limit)

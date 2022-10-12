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


router = APIRouter(prefix="/profile",
                   tags=["Profile"],
                   responses={**responses},
                   dependencies=[Depends(require_user)]
                   )


@router.get('/',
            response_model=user_schemas.ShowUser,
            status_code=status.HTTP_200_OK,
            )
def get_current_user_profile(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    """
    **Get Current User Profile** 
    - This operation obtains the information of the user logged within the app
    - **All Type of users** can access this route and verify their data

    ***Parameters*** :
    - Access Token

    **Response Model** :
    - user: ShowUser 

    **Return** 
    - id 
    - email
    - status
    - created_on
    - role id
    - role name
    - role created on

    from the current user logged 

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions.current_user_profile(db, current_user)


@router.patch("/update/password",
              status_code=status.HTTP_202_ACCEPTED,
              summary="Update Current User password",
              responses={202: {"model": schemas_config.GodMessage}}
              )
def update_me_password(
    request: user_schemas.UpdatePassMe,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """
    **Update Password**

    - This path operation update logged user password
    - Validate the actual password from current user
    - Validate confirmation from update a new password
    - **All Users** has access to this route.

    **Parameters**:
    - Access Token
    - Request body parameter:
    - **user: User** -> An User model with **actual_password**, **new_password**, **password_confirmation**

    Return 

    - **status code 202** 
    - **string message** 

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions.update_my_password(db, request, current_user)


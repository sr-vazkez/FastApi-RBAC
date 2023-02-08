from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.dependencies.data_conexion import get_db
from app.dependencies.verify_user import require_user
from app.internal.users import UsersActions
from app.schemas import schemas_config, user_schemas
from app.schemas.responses_schemas import responses


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    responses={**responses},
    dependencies=[Depends(require_user)],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.ShowUser,
    summary="Get current user information",
)
async def get_current_user_profile(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """**Get Current User Profile**.

    Get the user's information in session.

    - This operation obtains the information of the user
     logged within the app.
    - Users can access without having assigned a permit.

    **Parameters** :
    - Access Token

    **Response Model** :
    - user: **ShowUser**

    *Return*:
    - user: **ShowUser** -> A ShowUser model
     with: id (UUDI Format), email, is_active, created_on,
     role_id (UUDI Format), role_name
    - **status code** -> 200

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions().current_user_profile(db, current_user)


@router.patch(
    "/update/password",
    status_code=status.HTTP_202_ACCEPTED,
    responses={202: {"model": schemas_config.GoodMessage}},
    summary="Update Current User password",
)
async def update_me_password(
    request: user_schemas.UpdatePassMe,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """**Update Password**.

    Update the user's password in Session.

    - This path operation update logged user password
    - Validate the actual password from current user
    - Validate confirmation from update a new password
    - Users can access without having assigned a permit.

    **Parameters**:
    - Access Token

    Request body parameter:
    - user: **UpdatePassMe** -> An User model with
     **actual_password**, **new_password**, **password_confirmation**

    *Return*:
    - **JSON Response** -> succesfull message
    - **status code** -> 202

    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return UsersActions().update_my_password(db, request, current_user)

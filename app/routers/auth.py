from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from fastapi_another_jwt_auth import AuthJWT

from app.dependencies.data_conexion import get_db
from app.internal.auth import AuthActions
from app.dependencies.verify_user import require_user
from app.schemas import schemas_config, auth_schemas
from app.schemas import responses_schemas


router = APIRouter(prefix="/auth",
    tags=["Auth"],
    responses={**responses_schemas.responses}
)


@router.post(
    "/signing",
    responses={200: {"model": auth_schemas.ResponseAccessInfo}},
    response_model=auth_schemas.ResponseAccessInfo,
    summary="Login In the App"
)
def user_login(
    request: schemas_config.Login,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """
    **Login User** 

    - This path operation logs a user in the app
    - It provides us with an access token to be able to perform various actions within the app
    - The user must be pre-registered to be able to log
    - **All Type of users** can access this route

    **Parameters**:

    - *Request Body Parameter*:
        - user: Login -> *User email* and *User password* 

    **Returns** to the user with the following information:
    - **email** 
    - **user**
    - **status**
    - **user role**
    - **access token** 
    - **refresh token** 

    ***NOTE:***
    - The access token has a **2 hours** of live.
    - The refresh token has a **4 hours** of live.
    - To test the paths that ask for tokens in programs such as postman follow the following syntax:
    > Header: Authorization 

    > Value: Bearer token
    """
    return AuthActions.user_login(request,db, Authorize)


@router.get(
    "/refresh",
    summary="Generate a new access and refresh tokens",
    responses={200: {"model": auth_schemas.ResponseRefreshTokenInfo}},
    response_model=auth_schemas.ResponseRefreshTokenInfo
)
def refresh_token(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """
    **Refresh** 

    - This path operation asks for the refresh token of the user in session.
    - Only supports refresh tokens that are within session time (4 horas)
    - **All Type of users** can access this route
    - *Test this path in applications such as postman.* 
    - *For accessing /refresh endpoint remember*:
        - to change **access_token** with **refresh_token** in the ***header Authorization: Bearer <refresh_token>***

    **Parameters**:
    - refresh token

    **Return**:
    - Response Model:
        - ResponseTokenBase -> access token and refresh token
    """
    return AuthActions.refresh_token(db,Authorize)

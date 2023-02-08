from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_another_jwt_auth import AuthJWT
from sqlalchemy.orm import Session


from app.dependencies.data_conexion import get_db
from app.internal.auth import AuthActions
from app.schemas import auth_schemas, schemas_config, responses_schemas


router = APIRouter(
    prefix="/auth", tags=["Auth"], responses={**responses_schemas.responses}
)


@router.post(
    "/signing",
    status_code=status.HTTP_200_OK,
    responses={200: {"model": auth_schemas.ResponseAccessInfo}},
    response_model=auth_schemas.ResponseAccessInfo,
    summary="Login In the App",
)
async def user_login(
    request: schemas_config.Login,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
) -> JSONResponse:
    """**Login User**.

    Identify yourself in the application to get JWT Access

    - This enpoint logs a user in the app
    - It provides us with an access token to be able to
     perform various actions within the app
    - The user must be pre-registered to be able to log
    - **Open Endpoint**

    ***Important Information:***
    - The access token has a **2 hours** of live.
    - The refresh token has a **4 hours** of live.
    - To test the paths that ask for tokens in programs
     such as postman follow the following syntax:
        - ```Header: Authorization```
        - ```Value: Bearer token```

    **Parameters**:

    **Request Body Parameter**:
    - user: **Login** -> *User email* and *User password*

    *Returns*
    - auth: **ResponseAccessInfo** -> A ResponseAccessInfo model with: access_token,
     refresh_token, user_email, role_name, permissions(List of actions), searches
    - **status code** -> 200

    """
    return AuthActions().user_login(request, db, Authorize)


@router.get(
    "/refresh",
    status_code=status.HTTP_200_OK,
    responses={200: {"model": auth_schemas.ResponseRefreshTokenInfo}},
    response_model=auth_schemas.ResponseRefreshTokenInfo,
    summary="Generate a new access and refresh tokens",
)
async def refresh_token(
    db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
) -> JSONResponse:
    """**Refresh Token**.

    Refresh your user's session generating new JWT
     with new expiration hour.

    - This path operation asks for the refresh token of the user in session.
    - Only supports refresh tokens that are within session time (4 hours)
    - **Open Endpoint**

    ***Important Information:***
    - *Test this path in applications such as postman.*

    - *For accessing `/refresh` endpoint remember*:
        - to change **access_token** with **refresh_token**
         in the ```Header: Authorization```: ```Value: Bearer refresh token```

    **Parameters**:
    - Refresh token

    *Return*:
    - auth: **ResponseRefreshTokenInfo** -> A ResponseRefreshTokenInfo model
     with: access_token, refresh_token, user_email,
     role_name, permissions(List of actions), searches
    - **status code** -> 200

    """
    return AuthActions().refresh_token(db, Authorize)

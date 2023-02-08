from typing import List
from pydantic import BaseModel, EmailStr, Field


class ResponseToken(BaseModel):
    """ResponseToken.

    Args:
        BaseModel: Esta clase tiene las propiedades access_token
        y refresh_token para poderlas heredar en caso de construir una
        respuesta de json mas compleja.
    """

    access_token: str
    refresh_token: str


class ActionList(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        ActionList (BaseModel): Pydantic BaseModel
    """

    permissionName: List


class ResponseTokenData(ResponseToken):
    """ResponseTokenData.

    Args:
        ResponseToken: Esta clase le heredara su informacion asi
        que si se desea se puede utilizar esta clase para hacer una
        respuesta con los datos de esta clase y con los adicionales
        teniendo
    """

    user_email: EmailStr = Field(Example="email@email.com")
    role_name: str = Field(Example="root")
    permissions: ActionList


class ResponseRefreshTokenInfo(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool
    data: ResponseTokenData


class ResponseAccessInfo(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool
    data: ResponseTokenData

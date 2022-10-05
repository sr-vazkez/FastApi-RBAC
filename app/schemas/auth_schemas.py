from pydantic import BaseModel, EmailStr, Field


class ResponseToken(BaseModel):
    """ResponseToken

    Args:
        BaseModel: Esta clase tiene las propiedades access_token
        y refresh_token para poderlas heredar en caso de construir una
        respuesta de json mas compleja.
    """
    access_token: str
    refresh_token: str


class ResponseTokenData(ResponseToken):
    """ResponseTokenData

    Args:
        ResponseToken: Esta clase le heredara su informacion asi
        que si se desea se puede utilizar esta clase para hacer una 
        respuesta con los datos de esta clase y con los adicionales 
        teniendo 
    """
    #user_role: str
    #user_email: EmailStr = Field(Example="email@email.com")


class ResponseRefreshTokenInfo(BaseModel):
    success: bool
    data: ResponseToken


class ResponseAccessInfo(BaseModel):
    success: bool
    data: ResponseTokenData

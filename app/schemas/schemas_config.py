from pydantic import BaseModel, EmailStr, Field
from decouple import config


class Settings(BaseModel):
    """Settings 
    Esta clase es necesaria para poder
    cargar la key de los jwt tokens
    """
    authjwt_secret_key: str = config("secret")


class Login(BaseModel):
    # ESQUEMA PARA LOGGEARSE EN LA APP
    email: EmailStr = Field(
        ...,
        example="user@example.com"
    )
    password: str = Field(
        ...,
        min_length=8
    )


class Message(BaseModel):
    """
    Message
    Esta clase sirve para poder mostrar en la documentacion
    de swagger los posibles errores de nuestra api
    Ejemplo :
    * 404 : Not found
    """
    success: bool = Field(example=False)
    msg: str


class MessagePermissionError(BaseModel):
    success: bool = Field(example=False)
    msg: str


class MessagePermission(BaseModel):
    detail: MessagePermissionError


class GodMessage(BaseModel):
    """
    GodMessage
    Esta clase sirve para poder mostrar en la documentacion
    de swagger los codigos 2**  de nuestra api
    """
    success: bool = Field(example=True)
    msg: str

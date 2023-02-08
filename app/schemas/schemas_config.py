from pydantic import BaseModel, EmailStr, Field, BaseSettings
from decouple import config


class Settings(BaseModel):
    """Settings.

    Esta clase es necesaria para poder
    cargar la key de los jwt tokens

    Args:
        BaseModel (BaseModel): Pydantic BaseModel

    """

    authjwt_secret_key: str = config("secret")  # type: ignore


class SettingsDoc(BaseSettings):
    """SettingDoc Class.

    Esta clase modifica si se muestran o no la doc del API.

    Args:
        BaseSettings (Class): Overwritte env variables.
    """

    docs_url: str = config("docs_url")
    openapi_url: str = config("openapi_url")
    redoc_url: str = config("redoc_url")


class Login(BaseModel):
    """Login.

    Modelo de validcacion para el request del login.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, max_length=52)


class Message(BaseModel):
    """Message.

    Esta clase sirve para poder mostrar en la documentacion
    de swagger los posibles errores de nuestra api

    Ejemplo :
    * 404 : Not found

    Args:
        BaseModel (BaseModel): Pydantic BaseModel

    """

    success: bool = Field(example=False)
    msg: str


class MessagePermissionError(BaseModel):
    """Modelo para mostrar el error.

    En caso de no tener permisos suficientes

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = Field(example=False)
    msg: str


class MessagePermission(BaseModel):
    """Modelo para mostrar el error.

    En caso de no tener permisos suficientes

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    detail: MessagePermissionError


class GoodMessage(BaseModel):
    """GoodMessage.

    Esta clase sirve para poder mostrar en la documentacion
    de swagger los codigos 2**  de nuestra api
    """

    success: bool = Field(example=True)
    msg: str

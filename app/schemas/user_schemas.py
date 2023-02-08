from datetime import datetime
from uuid import UUID
from uuid import uuid4
from typing_extensions import Annotated
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, root_validator


class UserBase(BaseModel):
    """Modelo base para los objetos users.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """
    email: EmailStr = Field(...)

    class Config():
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """
        
        orm_mode = True


class Users(UserBase):
    """Modelo Que incluye el ID del user.

    Args:
        UserBase (BaseModel): : Herencia del modelo para
         evitar escribir mas.
    """
    
    id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]


class UserCreate(UserBase):
    """Modelo de validacion para crear users.

    Args:
        UserBase (BaseModel): Herencia del modelo para
         evitar escribir mas.
    """

    password: str = Field(
        ...,
        min_length=8
    )
    role_id: UUID = Field(
        ...,
        example="dff942ee-1f41-11ed-861d-0242ac120002"
    )


class UpdatePassMe(BaseModel):
    """Modelo de validacion para actualizar user's password.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    actual_password: str = Field(
        ...,
        min_length=8
    )
    new_password: str = Field(
        ...,
        min_length=8
    )
    password_confirmation: str = Field(
        ...,
        min_length=8
    )
    #!Custom Error

    @root_validator()
    def password_macth(vls, values):
        """Se valida que coincida el password actual.

        Args:
            vls (self): self value
            values (str): valores con los cuales realizamos
             la validacion

        Raises:
            ValueError: En caso de no cumplir la condicion
             se levanta una exception de tipo value.

        Returns:
            values: Si todo sale bien se regresan los valores.
        """
        new_password = values.get("new_password")
        password_confirmation = values.get("password_confirmation")
        if new_password != password_confirmation:
            raise ValueError('Password don´t macth')
        return values

    class Config():
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class UpdatePass(BaseModel):
    """Modelo de para actualizar user's password.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    new_password: str = Field(
        ...,
        min_length=8
    )
    password_confirmation: str = Field(
        ...,
        min_length=8
    )
    #!Custom Error

    @root_validator()
    def password_macth(vls, values):
        """Se valida que coincidan los passwords.

        Args:
            vls (self): self value
            values (str): valores con los cuales realizamos
             la validacion

        Raises:
            ValueError: En caso de no cumplir la condicion
             se levanta una exception de tipo value.

        Returns:
            values: Si todo sale bien se regresan los valores.
        """
        new_password = values.get("new_password")
        password_confirmation = values.get("password_confirmation")
        if new_password != password_confirmation:
            raise ValueError('Password don´t macth')
        return values


class UpdateUser(BaseModel):
    """Modelo de validacion para actualizar users.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    email: Optional[EmailStr] = Field(None, description="Email of the user")
    status: Optional[bool] = True

    class Config():
        orm_mode = True


class ShowInfoUser(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    email: EmailStr = Field(...)
    status: Optional[bool] = True
    created_on: datetime
    role_id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    role_name: Optional[str] = Field(None, description="Name of the role")
    role_created_on: Optional[datetime] = Field(
        None, description="Created on of the role")

    class Config():
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowUsers(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    numRows: int
    data: List[ShowInfoUser]

    class Config():
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowUser(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    data: ShowInfoUser

    class Config():
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowUserWithRole(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    data: ShowInfoUser

    class Config():
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """
        orm_mode = True

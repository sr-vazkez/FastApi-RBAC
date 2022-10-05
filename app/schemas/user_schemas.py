from datetime import datetime
from uuid import UUID
from uuid import uuid4
from typing_extensions import Annotated
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, root_validator


class UserBase(BaseModel):
    # Base del model User
    email: EmailStr = Field(...)

    class Config():
        orm_mode = True


class Users(UserBase):
    id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]


class UserCreate(UserBase):
    # Esquema para crear usuarios
    password: str = Field(
        ...,
        min_length=8
    )
    role_id: UUID = Field(
        ...,
        example="dff942ee-1f41-11ed-861d-0242ac120002"
    )


class UpdatePassMe(BaseModel):
    # Esquema que se usa para actualizar el password de un user
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
        new_password = values.get("new_password")
        password_confirmation = values.get("password_confirmation")
        if new_password != password_confirmation:
            raise ValueError('Password don´t macth')
        return values

    class Config():
        orm_mode = True


class UpdatePass(BaseModel):
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
        new_password = values.get("new_password")
        password_confirmation = values.get("password_confirmation")
        if new_password != password_confirmation:
            raise ValueError('Password don´t macth')
        return values


class UpdateUser(BaseModel):
    # SE UTILIZA PARA PODER  ACTUALIZAR LA INFORMACION DEL USER
    email: Optional[EmailStr] = Field(None, description="Email of the user")
    status: Optional[bool] = True

    class Config():
        orm_mode = True


class ShowInfoUser(BaseModel):
    # MOSTRAR USUARIOS
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
        orm_mode = True


class ShowUsers(BaseModel):
    success: bool = True
    numRows: int
    data: List[ShowInfoUser]

    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    success: bool = True
    data: ShowInfoUser

    class Config():
        orm_mode = True


class ShowUserWithRole(BaseModel):
    success: bool = True
    data: ShowInfoUser

    class Config():
        orm_mode = True

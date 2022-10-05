from datetime import datetime
from typing import List, Optional
#! To use in response_model
from uuid import uuid4
from pydantic import BaseModel, Field, EmailStr
from typing_extensions import Annotated


class RoleBase(BaseModel):
    # ? Base del model User
    name: str = Field(...)
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )

class RoleCreate(RoleBase):
    # ? Esquema para crear Roles
    #! Este Ta bien
    pass


class UpdateRole(RoleCreate):
    # ? SE UTILIZA PARA PODER  ACTUALIZAR LA INFORMACION DEL Role
    name: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )


class ShowRoleInfo(BaseModel):
    # ? MOSTRAR TODOS LOS ROLES
    id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    name: str = Field(...)
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )
    created_on: datetime


class ShowRole(BaseModel):
    success: bool = True
    data: ShowRoleInfo

    class Config():
        orm_mode = True


class ShowRoles(BaseModel):
    success: bool = True
    numRows: int
    data: List[ShowRoleInfo]

    class Config():
        orm_mode = True


class ShowRoleWithUser(ShowRoleInfo):
    user_id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    user_email: EmailStr = Field(...)
    user_status: bool
    user_created_on: datetime


class ShowRoleWithUsers(BaseModel):
    success: bool = True
    numRows: int
    data: List[ShowRoleWithUser]

    class Config():
        orm_mode = True

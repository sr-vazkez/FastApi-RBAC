from datetime import datetime
from typing import Annotated, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class ModuleBase(BaseModel):
    # Base del model User
    name: str = Field(...)
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )


class ModuleCreate(ModuleBase):
    pass


class UpdateModule(ModuleBase):
    name:Optional[str]#
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )


class ShowModuleInfo(BaseModel):
    # ? MOSTRAR TODOS LOS MODULOS
    id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    name: str = Field(...)
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )
    created_on: datetime

    class Config():
        orm_mode = True


class ShowModule(BaseModel):
    status: bool = True
    data: ShowModuleInfo

    class Config():
        orm_mode = True


class ShowModules(BaseModel):
    status: bool = True
    numRows: int
    data: List[ShowModuleInfo]

    class Config():
        orm_mode = True


class ShowModuleWithAction(ShowModuleInfo):
    action_id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    action_name: str 
    action_value: bool
    action_created_on: datetime


class ShowModuleWithActions(BaseModel):
    success: bool = True
    numRows: int 
    data: List[ShowModuleWithAction]

    class Config():
        orm_mode = True

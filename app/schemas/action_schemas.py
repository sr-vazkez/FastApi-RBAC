from app.models.actions_enum import ActionName
from datetime import datetime
from uuid import UUID
from uuid import uuid4
from typing_extensions import Annotated
from typing import List, Optional
from pydantic import BaseModel, Field


class ActionBase(BaseModel):
    action_name: str = Field(...)
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )
    value: bool = Field(
        example = True,
    )
    module_id: UUID = Field(
        ...,
        example="dff942ee-1f41-11ed-861d-0242ac120002"
    )

class ActionCreate(ActionBase):
    pass 

class UpdateAction(BaseModel):
    action_name: Optional[str] 
    value: bool = Field(example = True)
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )


class ShowActionInfo(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    action_name: str = Field(...)
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )
    value: bool
    created_on: datetime
    module_id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    module_name: str
    module_created_on: datetime



class ShowAction(BaseModel):
    success: bool = True
    data: ShowActionInfo
    class Config():
        orm_mode = True

class ShowActions(BaseModel):
    success: bool = True
    numRows: int
    data: List[ShowActionInfo]

    class Config():
        orm_mode = True 
from datetime import datetime
from uuid import UUID
from uuid import uuid4
from typing_extensions import Annotated
from typing import List, Optional
from pydantic import BaseModel, Field


class assigned_action(BaseModel):
    role_id: UUID = Field(
        ...,
        example="dff942ee-1f41-11ed-861d-0242ac120002"
    )

    actions_id: UUID = Field(
        ...,
        example="dff942ee-1f41-11ed-861d-0242ac120002"
    )
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )

class update_assigned_action_desc(BaseModel):
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )



class ShowRoleActionInfo(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    actions_id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    role_id: Annotated[str, Field(default_factory=lambda: uuid4(
    ).hex, example="dff942ee-1f41-11ed-861d-0242ac120002"), ]
    created_on: datetime
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )


class ShowRoleAction(BaseModel):
    success: bool = True
    data: ShowRoleActionInfo

    class Config():
        orm_mode = True

class ShowRoleActions(BaseModel):
    success: bool = True
    numRows: int
    data: List[ShowRoleActionInfo]

    class Config():
        orm_mode = True
from uuid import UUID
from uuid import uuid4
from typing_extensions import Annotated
from typing import List, Optional
from pydantic import BaseModel, Field


class assigned_action(BaseModel):
    """Modelo de validacion para crear permissions.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    role_id: UUID = Field(
        ..., example="dff942ee-1f41-11ed-861d-0242ac120002", description="Id from role"
    )

    actions_id: UUID = Field(
        ...,
        example="dff942ee-1f41-11ed-861d-0242ac120002",
        description="Id from action",
    )
    description: Optional[str] = Field(
        max_length=250, description="Optional text to explain a role in your app :D"
    )

    class Config:
        """Config class.

        Configuramos que todos los str sean en minusculas.
        """

        anystr_lower = True


class update_assigned_action_desc(BaseModel):
    """Modelo de validacion para actualizar permissions.

    Solo actualizamo la descripcion.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    description: Optional[str] = Field(
        max_length=250, description="Optional text to explain a role in your app :D"
    )

    class Config:
        """Config class.

        Configuramos que todos los str sean en minusculas.
        """

        anystr_lower = True


class ShowRoleActionInfo(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    id: Annotated[
        str,
        Field(
            default_factory=lambda: uuid4().hex,
            example="dff942ee-1f41-11ed-861d-0242ac120002",
        ),
    ]
    actions_id: Annotated[
        str,
        Field(
            default_factory=lambda: uuid4().hex,
            example="dff942ee-1f41-11ed-861d-0242ac120002",
        ),
    ]
    role_id: Annotated[
        str,
        Field(
            default_factory=lambda: uuid4().hex,
            example="dff942ee-1f41-11ed-861d-0242ac120002",
        ),
    ]
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )


class ShowRoleAction(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    data: ShowRoleActionInfo

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowRoleActions(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    numRows: int
    data: List[ShowRoleActionInfo]

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True

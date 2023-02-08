from uuid import UUID
from uuid import uuid4
from typing_extensions import Annotated
from typing import List, Optional
from pydantic import BaseModel, Field


class ActionBase(BaseModel):
    """Modelo base para los objetos Actions.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    action_name: str = Field(
        ..., min_length=3, max_length=200, description="Name for the action"
    )
    description: Optional[str] = Field(
        min_length=3,
        max_length=250,
        description="Optional text to explain a role in your app :D",
    )
    is_active: bool = Field(example=True, description="For active or desactive action")
    module_id: UUID = Field(
        ...,
        example="dff942ee-1f41-11ed-861d-0242ac120002",
        description="Id from module",
    )

    class Config:
        """Config class.

        Configuramos que todos los str sean en minusculas.
        """

        anystr_lower = True


class ActionCreate(ActionBase):
    """Modelo de validacion para crear actions.

    Args:
        ActionBase (BaseModel): Herencia del modelo para
         evitar escribir mas.
    """

    pass


class UpdateAction(BaseModel):
    """Modelo de validacion para actualizar actions.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    action_name: Optional[str] = Field(
        max_length=200, description="Name for the action"
    )
    is_active: bool = Field(example=True, description="For active or desactive action")
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )

    class Config:
        """Config class.

        Configuramos que todos los str sean en minusculas.
        """

        anystr_lower = True


class ShowActionInfo(BaseModel):
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
    action_name: str = Field(...)
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )
    is_active: bool
    module_id: Annotated[
        str,
        Field(
            default_factory=lambda: uuid4().hex,
            example="dff942ee-1f41-11ed-861d-0242ac120002",
        ),
    ]
    module_name: str


class ShowAction(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    data: ShowActionInfo

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowActions(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    numRows: int
    data: List[ShowActionInfo]

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True

from typing import Annotated, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class ModuleBase(BaseModel):
    """Modelo base para los objetos Modules.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    name: str = Field(
        ..., min_length=3, max_length=200, description="For give name a module"
    )
    description: Optional[str] = Field(
        max_length=250, description="Optional text to explain a role in your app :D"
    )

    class Config:
        """Config class.

        Configuramos que todos los str sean en minusculas.
        """

        anystr_lower = True


class ModuleCreate(ModuleBase):
    """Modelo de validacion para crear modules.

    Args:
        ModuleBase (BaseModel): Herencia del modelo para
         evitar escribir mas.
    """

    pass


class UpdateModule(BaseModel):
    """Modelo de validacion para actualizar modules.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    name: Optional[str] = Field(max_length=200, description="For give name a module")
    description: Optional[str] = Field(
        max_length=250, description="Optional text to explain a role in your app :D"
    )

    class Config:
        """Config class.

        Configuramos que todos los str sean en minusculas.
        """

        anystr_lower = True


class ShowModuleInfo(BaseModel):
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
    name: str = Field(..., min_length=3, max_length=250)
    description: Optional[str] = Field(
        max_length=250, description="Optional text to explain a role in your app :D"
    )

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowModule(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    data: ShowModuleInfo

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowModules(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    numRows: int
    data: List[ShowModuleInfo]

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowModuleWithAction(ShowModuleInfo):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    action_id: Annotated[
        str,
        Field(
            default_factory=lambda: uuid4().hex,
            example="dff942ee-1f41-11ed-861d-0242ac120002",
        ),
    ]
    action_name: str
    action_is_active: bool


class ShowModuleWithActions(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    numRows: int
    data: List[ShowModuleWithAction]

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True

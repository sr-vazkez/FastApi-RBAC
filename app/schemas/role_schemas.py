from typing import List, Optional

# To use in response_model
from uuid import uuid4
from pydantic import BaseModel, Field, EmailStr
from typing_extensions import Annotated


class RoleBase(BaseModel):
    """Modelo base para los objetos Role.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    name: str = Field(
        ..., min_length=3, max_length=200, description="Name for your role"
    )
    description: Optional[str] = Field(
        max_length=250, description="Optional text to explain a role in your app :D"
    )

    class Config:
        """Config class.

        Configuramos que todos los str sean en minusculas.
        """

        anystr_lower = True


class RoleCreate(RoleBase):
    """Modelo de validacion para crear Roles.

    Args:
        RoleBase (BaseModel): Herencia del modelo para
         evitar escribir mas.
    """

    pass


class UpdateRole(BaseModel):
    """Modelo de validacion para actualizar roles.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    name: Optional[str] = Field(
        max_length=200, description="Optional text to explain a role in your app :D"
    )
    description: Optional[str] = Field(
        max_length=250, description="Optional text to explain a role in your app :D"
    )

    class Config:
        """Config class.

        Configuramos que todos los str sean en minusculas.
        """

        anystr_lower = True


class ShowRoleInfo(BaseModel):
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
    name: str = Field(...)
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )


class ActionInfo(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    permission_id: Annotated[
        str,
        Field(
            default_factory=lambda: uuid4().hex,
            example="dff942ee-1f41-11ed-861d-0242ac120002",
        ),
    ]
    module_name: str
    action_name: str


class ShowRoleInfoPermissions(BaseModel):
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
    name: str = Field(...)
    description: Optional[str] = Field(
        description="Optional text to explain a role in your app :D"
    )
    permissions: List[ActionInfo] = Field(
        description="Optional list of permissions assigned"
    )


class ShowRoleWithPermission(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    data: ShowRoleInfoPermissions

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowRole(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    data: ShowRoleInfo

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowRoles(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    numRows: int
    data: List[ShowRoleInfo]

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True


class ShowRoleWithUser(ShowRoleInfo):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    user_id: Annotated[
        str,
        Field(
            default_factory=lambda: uuid4().hex,
            example="dff942ee-1f41-11ed-861d-0242ac120002",
        ),
    ]
    user_email: EmailStr = Field(...)
    user_is_active: bool


class ShowRoleWithUsers(BaseModel):
    """Modelo de validacion al mostrar propiedades.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    success: bool = True
    numRows: int
    data: List[ShowRoleWithUser]

    class Config:
        """Habilitamos el modo orm.

        Para no tener problemas con el ORM.
        """

        orm_mode = True

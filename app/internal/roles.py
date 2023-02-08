from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.sql.expression import false, true
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app import main
from app.models.users import Users
from app.models.roles import Role
from app.models.actions import Actions
from app.models.module import Module
from app.models.role_actions import Role_Actions
from app.schemas import role_schemas

extra = {"event.category": "app_log"}


class RoleActions:
    """Esta clase realiza operacions en roles.

    Podemos crear, actualizar ,eliminar y editar ademas de
     generar otras acciones adiciionales.
    """

    def __init__(
        self,
        db: Optional[Session] = None,
        request: Optional[role_schemas.RoleCreate] = None,
        current_user: Optional[str] = None,
        start: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> None:
        self.db: Optional[Session] = db
        self.request: Optional[role_schemas.RoleCreate] = request
        self.current_user: Optional[str] = current_user
        self.start: Optional[int] = start
        self.limit: Optional[int] = limit

    def create_new_role(
        self, db: Session, request: role_schemas.RoleCreate, current_user: str
    ) -> JSONResponse:
        """Este metodo lo que hace es crear un role.

        Se pide el current_user para tener llenados
        la informacion para los datos de auditoria.

        #? Endpoint /roles/create POST

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            request (Pydantic model): Modelo de pydantic para recibir la
            informacion proporcionada por el frontend o el usuario.
            current_user (str): Este argumento es el ID del usuario el cual es un GUID
            se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
             y la propiedad msg con sus respectivos valores.
             En caso contrario nos mostrara la propiedad success y la propiedad msg.
        """
        new_role = db.query(Role).filter(Role.name == request.name).first()

        if new_role is not None and new_role.is_deleted is True:
            #  If the role is deleted. We can restore it and set the is_deleted to false
            new_role.is_deleted = False
            new_role.description = request.description
            new_role.created_by = current_user
            db.commit()
            main.logger.info(msg="Role created successfully!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"success": True, "msg": "Role created succesfully!"},
            )

        elif new_role is not None and new_role.is_deleted is False:
            #  If the role is not deleted, we can not create it.
            main.logger.info(msg="Role already exist!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "Role already exists!"},
            )

        new_role = Role(
            name=request.name,
            description=request.description,
            created_on=datetime.now(),
            created_by=current_user,
        )
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        main.logger.info(msg="Role created succesfully!", extra=extra)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"success": True, "msg": "role created succesfully!"},
        )

    def get_all_roles(
        self,
        db: Session,
        start: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> JSONResponse:
        """Este metodo cuenta todos los registros y paginar el listado de la informacion.

        #? ENDPOINT /roles/ GET

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            start (int, optional): Este argumento sirve para
            indicar el inicio de nuestro paginador. Defaults to None.
            limit (int, optional): Este argumento sirve para
            indicar el limite de nuestro paginador. Defaults to None.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
             en caso de tener exito nos mostarara la propiedad numRows con la cantidad
             de todos los registros y data con la informacion solicitada.
        """
        show_roles = (
            db.query(Role)
            .filter(Role.name != "super admin")
            .filter_by(is_deleted=False)
            .offset(start)
            .limit(limit)
            .all()
        )

        total = len(show_roles)
        main.logger.info(msg="List of Roles is display!", extra=extra)
        res = {"success": True, "numRows": total, "data": show_roles}

        return jsonable_encoder(res)

    def get_one_role(self, db: Session, id: UUID) -> JSONResponse:
        """Este metodo lo que hace es realizar la busqueda de un registro por su id.

        #? ENDPOINT /roles/{id} GET

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa algo que
            no se encuentre en este formato sera invalido.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success en caso
             de tener exito nos mostarara la propiedad data con la informacion del usuario buscado.
        """
        role = (
            db.query(Role)
            .filter(Role.name != "super admin")
            .filter(Role.id == id)
            .filter_by(is_deleted=False)
            .first()
        )

        if not role:
            main.logger.info(msg=f"Role {id} not found!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )

        res = {"success": True, "data": role}
        main.logger.info(msg=f"Role {id} is found!", extra=extra)
        return jsonable_encoder(res)

    def update_role_info(
        self,
        db: Session,
        id: UUID,
        request: role_schemas.UpdateRole,
        current_user: str,
    ) -> JSONResponse:
        """Este metodo realiza la actualizacion de datos sobre un registro.

        Filtrado por su id, se pide el current_user para tener llenados la informacion
        para los datos de auditoria.

        #? ENDPOINT /roles/{id} PUT

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY.
            Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa
            algo que no se encuentre en este formato sera invalido.
            request (Pydantic model): Modelo de pydantic para recibir la
            informacion proporcionada por el frontend o el usuario.
            current_user (str): Este argumento es el ID del usuario el cual
            es un GUID se obtiene  con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
            y la propiedad msg con sus respectivos valores. En caso contrario nos mostrara
            la propiedad success y la propiedad msg.
        """
        # Buscamos el rol el cual es filtrado por un id
        role = (
            db.query(Role)
            .filter(Role.id == id)
            .filter(Role.is_deleted == false())
            .first()
        )
        # Si no existe devolvemos un error
        if not role:
            main.logger.info(msg=f"Role {id} not found!", extra=extra)
            # Si no lo encuentra regresamos
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )
        # Verificar si existe el role
        if request.name != role.name:
            if db.query(Role).filter(Role.name == request.name).first():
                main.logger.info(
                    msg=f"Role {request.name} already exists!", extra=extra
                )
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"success": True, "msg": "Choose Another Name!"},
                )

        if request.name is None or request.name == "":
            request.name = role.name

        # Pero si lo encuentra. Actualiza!
        role.description = request.description
        role.name = request.name
        role.updated_by = current_user
        role.updated_on = datetime.now()
        db.add(role)
        db.commit()
        main.logger.info(msg="Role Updated successfully!", extra=extra)
        return JSONResponse(
            status_code=202, content={"success": True, "msg": "Updated successfully"}
        )

    def delete_one_role(self, db: Session, id: UUID) -> Optional[JSONResponse]:
        """Este metodo lo que hace es eliminar un registro (soft-deleted).

        Filtrandolo por su id en formato GUID V4

        #? ENDPOINT /roles/{id}/delete/ DELETE
        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY.
            Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa
            algo que no se encuentre en este formato sera invalido.
            current_user (str): Este argumento es el ID del usuario el cual
            es un GUID se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            Optional[JSONResponse]: status code 204 NO CONTENT el método DELETE
             regresa NONE en caso de algun erro devolvemos un JSONRESPONSE.
        """
        check_child = (
            db.query(Users)
            .filter(Users.role_id == id)
            .filter(Users.is_deleted == false())
            .count()
        )

        # print(check_child)

        if check_child >= 1:
            # print("No puedes borrarlo hasta borrar los registros hijos")
            main.logger.info(
                "Cannot delete this element because the child element must be deleted first"
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "First Delete Users assigned!!"},
            )

        is_d = True
        role = db.query(Role).filter(Role.id == id).filter_by(is_deleted=False)

        if is_d is False:
            main.logger.info(
                msg="value is true but something was changed to false!", extra=extra
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "Its not possible!"},
            )

        if not role.first():
            main.logger.info(msg=f"Role {id} not found", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )

        role.update({Role.is_deleted: is_d})
        db.commit()
        main.logger.info(msg=f"Role {id} it's deleted!", extra=extra)
        return None

    def show_role_with_users(
        self,
        db: Session,
        id: UUID,
        start: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> JSONResponse:
        """Esta funcion lo que hace es filtrar un registro por su id en GUID.

        Una vez que lo encuentra lo que realiza es traer a todos estos datos
        relacionados los cuales se pueden ir filtrando :D.

        #? ENDPOINT  /roles/{id}/users
        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY.
            Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa
            algo que no se encuentre en este formato sera invalido.
            start (int, optional): Este argumento sirve para
            indicar el inicio de nuestro paginador. Defaults to None.
            limit (int, optional): Este argumento sirve para
            indicar el limite de nuestro paginador. Defaults to None.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
                en caso de tener exito nos mostarara la propiedad numRows con la cantidad de todos
                los registros y data con la informacion solicitada.
        """
        show_role_with_users = (
            db.query(
                Role.id,
                Role.name,
                Role.description,
                Users.id.label("user_id"),
                Users.email.label("user_email"),
                Users.is_active.label("user_is_active"),
            )
            .join(Role, isouter=True)
            .filter(Role.id == id)
            .filter(Users.is_deleted == false())
            .filter(Role.is_deleted == false())
            .offset(start)
            .limit(limit)
            .all()
        )

        total = len(show_role_with_users)

        res = {"success": True, "numRows": total, "data": show_role_with_users}
        main.logger.info(msg="List of Users from Role is display!", extra=extra)
        return jsonable_encoder(res)

    def show_actions_and_modules(self, db: Session, id: UUID) -> JSONResponse:
        """El método show_actions_and_modules lo que hace es filtrar el registro por ID.

        Con ello nos trae sus modulos asignados y el nombre de las acciones que tiene.

        #? ENDPOINT /roles/{id}/permissions/ GET

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4
             si se ingresa algo que no se encuentre en este formato sera invalido.
            start (int, optional): Este argumento sirve para indicar el inicio de nuestro paginador.
             Defaults to None.
            limit (int, optional): Este argumento sirve para indicar el limite de nuestro paginador.
             Defaults to None.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
             en caso de tener exito nos mostarara la propiedad numRows con la cantidad de todos
             los registros y data con la informacion solicitada.
        """
        role = (
            db.query(Role.id, Role.name, Role.description)
            .filter(Role.id == id)
            .filter_by(is_deleted=False)
            .first()
        )

        if role is None:
            main.logger.info(msg=f"Role {id} No exits!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )

        permission = (
            db.query(
                Role_Actions.id.label("permission_id"),
                Module.name.label("module_name"),
                Actions.action_name,
            )
            .order_by(Module.name)
            .join(Role_Actions, isouter=False)
            .join(Module, isouter=False)
            .filter(Role_Actions.role_id == role.id.__str__())
            .filter(Role_Actions.actions_id == Actions.id)
            .filter(Actions.module_id == Module.id)
            .filter(Actions.is_deleted == false())
            .filter(Actions.is_active == true())
            .filter(Module.is_deleted == false())
            .filter(Role_Actions.is_deleted == false())
            .all()
        )

        res = {
            "success": True,
            "data": {
                "id": role.id,
                "name": role.name,
                "description": role.description,
                "permissions": permission,
            },
        }
        main.logger.info(msg="List permissions in role", extra=extra)
        return jsonable_encoder(res)

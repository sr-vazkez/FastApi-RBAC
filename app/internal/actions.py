from datetime import datetime
from typing import Optional
from uuid import UUID


from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app import main
from app.schemas import action_schemas
from app.models.module import Module
from app.models.actions import Actions
from app.models.role_actions import Role_Actions

extra = {"event.category": "app_log"}


class ActionsOperations:
    """Esta clase realiza operacions en Actions.

    Podemos crear, actualizar ,eliminar y editar ademas de
     generar otras acciones adiciionales.
    """

    def __init__(
        self,
        db: Optional[Session] = None,
        request: Optional[action_schemas.ShowActions] = None,
        current_user: Optional[str] = None,
        start: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> None:
        self.db: Optional[Session] = db
        self.request: Optional[action_schemas.ShowActions] = request
        self.current_user: Optional[str] = current_user
        self.start: Optional[int] = start
        self.limit: Optional[int] = limit

    def create_new_action(
        self, db: Session, current_user: str, request: action_schemas.ActionCreate
    ) -> JSONResponse:
        """Este metodo lo que hace es crear una accion.

        Se pide el current_user para tener llenados la informacion para los datos de auditoria.

        #? Endpoint /actions/create POST

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            current_user (str): Este argumento es el ID del usuario el cual es un GUID
             se obtiene con la clase Authorize y el metodo get_jwt_subject()
            request (Pydantic model): Modelo de pydantic para recibir la informacion proporcionada
             por el frontend o el usuario.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success y
             la propiedad msg con sus respectivos valores.
             En caso contrario nos mostrara la propiedad success
             y la propiedad msg.
        """
        new_action = (
            db.query(Actions)
            .filter(
                Actions.module_id == request.module_id,
                Actions.action_name == request.action_name,
            )
            .first()
        )

        # print(50*'-')
        # print(new_action)
        # print(50*'-')

        check_module = (
            db.query(Module.id)
            .filter(Module.id == request.module_id)
            .filter(Module.is_deleted == false())
            .first()
        )

        # print(50*'-')
        # print(check_module)
        # print(50*'-')

        if new_action and new_action.is_deleted is True:
            # If the action is deleted, we can restore it and set the is_deleted to False.
            # print("If the action is deleted, we can restore it.")
            new_action.is_deleted = False
            new_action.created_on = datetime.now()
            new_action.created_by = current_user
            db.commit()
            main.logger.info(msg="Action created successfully!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"success": True, "msg": "Action created succesfully!"},
            )

        elif new_action is not None and new_action.is_deleted is False:
            # If the user is not deleted, we can not create it.
            # print("If the user is not deleted, we can not create it.")
            main.logger.info(msg="Action already exist!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"success": True, "msg": "Action already exist!"},
            )

        elif not check_module:
            main.logger.info(msg="Invalid Module!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "Invalid Module!"},
            )

        new_action = Actions(
            action_name=request.action_name,
            description=request.description,
            is_active=request.is_active,
            module_id=request.module_id,
            created_on=datetime.now(),
            created_by=current_user,
        )
        db.add(new_action)
        db.commit()
        db.refresh(new_action)
        main.logger.info(msg="Action created succesfully!", extra=extra)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"success": True, "msg": "Actions created succesfully!"},
        )

    def get_all_actions(
        self,
        db: Session,
        start: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> JSONResponse:
        """Este metodo cuenta todos los registros y paginar el listado de la informacion.

        #? ENDPOINT /actions/ GET
        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            start (int, optional): Este argumento sirve para
            indicar el inicio de nuestro paginador. Defaults to None.
            limit (int, optional): Este argumento sirve para
            indicar el limite de nuestro paginador. Defaults to None.

        Returns:
            JSONResponse:  Nos devuelve una respuesta en JSON con la propiedad success
                en caso de tener exito nos mostarara la propiedad numRows con la cantidad de todos
                los registros y data con la informacion solicitada.
        """
        show_roles = (
            db.query(
                Actions.id,
                Actions.action_name,
                Actions.is_active,
                Actions.description,
                Actions.module_id,
                Module.name.label("module_name"),
            )
            .join(Module, isouter=True)
            .filter(Actions.is_deleted == false())
            .filter(Module.is_deleted == false())
            .offset(start)
            .limit(limit)
            .all()
        )
        # Sacar el numero de registros
        total = len(show_roles)

        res = {"success": True, "numRows": total, "data": show_roles}
        main.logger.info(msg="List of Actions is display!", extra=extra)
        return jsonable_encoder(res)

    def get_one_action(self, db: Session, id: UUID) -> JSONResponse:
        """Este metodo lo que hace es realizar la busqueda de un registro por su id.

        #? ENDPOINT /actions/{id} GET

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa algo que
            no se encuentre en este formato sera invalido.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
             en caso de tener exito nos mostarara la propiedad data con la informacion
             de la accion solicitada.
        """
        action = (
            db.query(
                Actions.id,
                Actions.action_name,
                Actions.is_active,
                Actions.description,
                Actions.module_id,
                Module.name.label("module_name"),
            )
            .join(Module, isouter=True)
            .filter(Actions.id == id)
            .filter(Actions.is_deleted == false())
            .filter(Module.is_deleted == false())
            .first()
        )

        if not action:
            main.logger.info(msg=f"Action {id} not found!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )

        res = {"success": True, "data": action}
        main.logger.info(msg=f"Action {id} is found!", extra=extra)
        return jsonable_encoder(res)

    def update_action_info(
        self,
        db: Session,
        id: UUID,
        request: action_schemas.UpdateAction,
        current_user: str,
    ) -> JSONResponse:
        """Este metodo realiza la actualizacion de datos sobre un registro filtrado por su id.

        Se pide el current_user para tener llenados la informacion para los datos de auditoria.

        #? ENDPOINT /actions/{id} PUT

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
        # Buscamos a un user por su id, este no debe de estar marcado como eliminado
        # Buscamos la accion de un modulo el cual es filtrado por un id
        # Si es que el usuario quiso no mandar el action_name lo dejamos por el actual
        action = (
            db.query(Actions)
            .filter(Actions.id == id)
            .filter(Actions.is_deleted == false())
            .first()
        )

        # Si no lo encuentra regresamos un error
        if not action:
            main.logger.info(msg=f"Action {id} not found!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )

        check_action_module = (
            db.query(Actions)
            .filter(Actions.action_name == request.action_name)
            .filter(Actions.module_id == action.module_id)
            .filter(Actions.is_deleted == false())
            .count()
        )

        if check_action_module >= 1:
            main.logger.info(msg="Action already exist!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"success": True, "msg": "Action already exist!"},
            )

        # Si es que el usuario quiso no mandar el action_name lo dejamos por el actual en la bd
        if request.action_name is None or request.action_name == "":
            request.action_name = action.action_name

        # Actualiza!
        action.action_name = request.action_name
        action.description = request.description
        action.is_active = request.is_active
        action.updated_by = current_user
        action.updated_on = datetime.now()
        db.add(action)
        db.commit()
        db.refresh(action)
        main.logger.info(msg="Action Updated successfully!", extra=extra)
        return JSONResponse(
            status_code=202, content={"success": True, "msg": "Updated successfully"}
        )

    def delete_one_action(self, db: Session, id: UUID) -> Optional[JSONResponse]:
        """Este metodo lo que hace es eliminar un registro (soft-deleted).

        Filtrandolo por su id en formato GUID V4

        #? ENDPOINT /actions/{id}/delete/ DELETE

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY.
            Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa
            algo que no se encuentre en este formato sera invalido.
            current_user (str): Este argumento es el ID del usuario el cual
            es un GUID se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            Optional[JSONResponse]: status code 204 NO CONTENT para usar el método DELETE
             es necesario regresas NONE en nuestros métodos.
        """
        check_child = (
            db.query(Role_Actions)
            .filter(Role_Actions.actions_id == id)
            .filter(Role_Actions.is_deleted == false())
            .count()
        )

        if check_child >= 1:
            # print("No puedes borrarlo hasta borrar los registros hijos")
            main.logger.info(
                "Cannot delete this element because the child element must be deleted first"
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "First Delete Permission assigned!!"},
            )

        is_d = True
        action = db.query(Actions).filter(Actions.id == id).filter_by(is_deleted=False)
        if is_d is False:
            main.logger.info(
                msg="value is true but something was changed to false!", extra=extra
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "Its not possible!"},
            )
        if not action.first():
            main.logger.info(msg=f"Action {id} not found", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )
        action.update({Actions.is_deleted: is_d, Actions.is_active: False})
        db.commit()
        main.logger.info(msg=f"Action {id} it's deleted!", extra=extra)
        return None

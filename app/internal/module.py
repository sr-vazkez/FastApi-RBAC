from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.sql.expression import false
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app import main
from app.models.module import Module
from app.models.actions import Actions
from app.schemas import module_schemas

extra = {"event.category": "app_log"}


class ModuleActions:
    """Esta clase realiza operacions en Modulos.

    Podemos crear, actualizar ,eliminar y editar ademas de
     generar otras acciones adiciionales.
    """

    def __init__(
        self,
        db: Optional[Session] = None,
        request: Optional[module_schemas.ShowModule] = None,
        current_user: Optional[str] = None,
        start: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> None:
        self.db: Optional[Session] = db
        self.request: Optional[module_schemas.ShowModule] = request
        self.current_user: Optional[str] = current_user
        self.start: Optional[int] = start
        self.limit: Optional[int] = limit

    def create_module(
        self, db: Session, request: module_schemas.ModuleCreate, current_user: str
    ) -> JSONResponse:
        """Este metodo lo que hace es crear un modulo.

        Se pide el current_user para tener llenados la informacion para los datos de auditoria.

        #? Endpoint /modules/create POST

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY.
             Defaults to Depends().
            request (Pydantic model): Modelo de pydantic para recibir la
             informacion proporcionada por el frontend o el usuario.
            current_user (str): Este argumento es el ID del usuario el
             cual es un GUID
            se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad
             success y la propiedad msg con sus respectivos valores.
             En caso contrario nos mostrara la propiedad success y la propiedad msg.
        """
        new_module = db.query(Module).filter(Module.name == request.name).first()

        if new_module is not None and new_module.is_deleted is True:
            #  If the module is deleted. We can restore it and set the is_deleted to false
            new_module.description = request.description
            new_module.is_deleted = False
            new_module.created_by = current_user
            db.commit()
            main.logger.info(msg="Module created successfully!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"success": True, "msg": "Module created succesfully!"},
            )
        elif new_module is not None and new_module.is_deleted is False:
            #  If the module is not deleted, we can not create it.
            main.logger.info(msg="Module already exist!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "Module already exist!"},
            )

        new_module = Module(
            name=request.name,
            description=request.description,
            created_on=datetime.now(),
            created_by=current_user,
        )
        db.add(new_module)
        db.commit()
        db.refresh(new_module)
        main.logger.info(msg="Module created succesfully!", extra=extra)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"success": True, "msg": "Module created succesfully!"},
        )

    def get_all_modules(
        self,
        db: Session,
        start: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> JSONResponse:
        """Este metodo cuenta todos los registros y paginar el listado de la informacion.

        #? ENDPOINT /modules/ GET

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
        show_modules = (
            db.query(Module)
            .filter_by(is_deleted=False)
            .offset(start)
            .limit(limit)
            .all()
        )

        total = len(show_modules)

        res = {"success": True, "numRows": total, "data": show_modules}
        main.logger.info(msg="List of Modules is display!", extra=extra)
        return jsonable_encoder(res)

    def get_one_module(self, db: Session, id: UUID) -> JSONResponse:
        """Este metodo lo que hace es realizar la busqueda de un registro por su id.

        #? ENDPOINT /modules/{id} GET

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa algo que
            no se encuentre en este formato sera invalido.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
             en caso de tener exito nos mostarara la propiedad data con la informacion
             del usuario buscado.
        """
        module = (
            db.query(Module).filter(Module.id == id).filter_by(is_deleted=False).first()
        )

        if not module:
            main.logger.info(msg=f"Module {id} not found!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )

        res = {"success": True, "data": module}
        main.logger.info(msg=f"Module {id} is found!", extra=extra)

        return jsonable_encoder(res)

    def update_module_info(
        self,
        db: Session,
        id: UUID,
        request: module_schemas.UpdateModule,
        current_user: str,
    ) -> JSONResponse:
        """Este metodo realiza la actualizacion de datos sobre un registro.

        Filtrado por su id, se pide el current_user para tener llenados la informacion
        para los datos de auditoria.

        #? ENDPOINT /modules/{id} PUT

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
        # Buscamos el email de un usuario el cual es filtrado por un id
        module = (
            db.query(Module)
            .filter(Module.id == id)
            .filter(Module.is_deleted == false())
            .first()
        )
        # estamos buscando primero por id
        if not module:
            main.logger.info(msg=f"Module {id} not found!", extra=extra)
            # Si no lo encuentra regresamos
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )
        # Verificar si ya existe
        if request.name != module.name:
            if db.query(Module).filter(Module.name == request.name).first():
                main.logger.info(
                    msg=f"Module {request.name} already exists!", extra=extra
                )
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"success": True, "msg": "Choose Another Name!"},
                )
        if request.name is None or request.name == "":
            request.name = module.name

        # Pero si lo encuentra. Actualiza!
        module.description = request.description
        module.name = request.name
        module.updated_by = current_user
        module.updated_on = datetime.now()
        db.add(module)
        db.commit()
        main.logger.info(msg="Module Updated successfully!", extra=extra)
        return JSONResponse(
            status_code=202, content={"success": True, "msg": "Updated successfully"}
        )

    def deleted_one_module(self, db: Session, id: UUID) -> Optional[JSONResponse]:
        """Este metodo lo que hace es eliminar un registro (soft-deleted).

        #? ENDPOINT /modules/{id}/delete/ DELETE

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY.
            Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa
            algo que no se encuentre en este formato sera invalido.
            current_user (str): Este argumento es el ID del usuario el cual
            es un GUID se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            Optional[JSONResponse]: status code 204 NO CONTENT el método DELETE
             es necesario regresas NONE en caso de algun erro devolvemos un JSONRESPONSE.
        """
        check_child = (
            db.query(Actions)
            .filter(Actions.module_id == id)
            .filter(Actions.is_deleted == false())
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
                content={"success": False, "msg": "First Delete Actions assigned!!"},
            )

        is_d = True
        module = db.query(Module).filter(Module.id == id).filter_by(is_deleted=False)
        if is_d is False:
            main.logger.info(
                msg="value is true but something was changed to false!", extra=extra
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "Its not possible!"},
            )

        if not module.first():
            main.logger.info(msg=f"Module {id} not found", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )
        module.update({Module.is_deleted: is_d})
        db.commit()
        main.logger.info(msg=f"Module {id} it's deleted!", extra=extra)
        return None

    def show_module_with_action(
        self,
        db: Session,
        id: UUID,
        start: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> JSONResponse:
        """Esta funcion lo que hace es filtrar un registro por su id en GUID.

        Una vez que lo encuentra lo que realiza es traer a todos estos datos
        relacionados los cuales se pueden ir filtrando :D.

        #? ENDPOINT  /modules/{id}/actions

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
        show_module_with_actions = (
            db.query(
                Module.id,
                Module.name,
                Module.description,
                Actions.id.label("action_id"),
                Actions.action_name.label("action_name"),
                Actions.is_active.label("action_is_active"),
            )
            .join(Module, isouter=True)
            .filter(Module.id == id)
            .filter(Actions.is_deleted == false())
            .filter(Module.is_deleted == false())
            .offset(start)
            .limit(limit)
            .all()
        )

        total = len(show_module_with_actions)

        res = {"success": True, "numRows": total, "data": show_module_with_actions}
        main.logger.info(msg="List of Actions from module is display!", extra=extra)
        return jsonable_encoder(res)

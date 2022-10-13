from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models.users import Users
from app.models.roles import Role
from app.models.actions import Actions
from app.models.module import Module
from app.models.role_actions import Role_Actions

from app.schemas import role_schemas


class RoleActions():
    @staticmethod
    def create_new_role(
        db: Session, 
        request: role_schemas.RoleCreate, 
        current_user: str
    ) -> JSONResponse:
        """Este metodo lo que hace es crear un role, 
        se pide el current_user para tener llenados
        la informacion para los datos de auditoria. 

        #? Endpoint /roles/create POST

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            request (Pydantic model): Modelo de pydantic para recibir la 
            informacion proporcionada por el frontend o el usuario.
            current_user (str): Este argumento es el ID del usuario el cual es un GUID 
            se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success y la propiedad msg con sus respectivos valores. En caso contrario nos mostrara la propiedad success y la propiedad msg.
        """
        request.name.lower()
        new_role = db.query(Role).filter(
            Role.name == request.name.lower()).first()

        if new_role is not None and new_role.is_deleted == True:
            #! If the role is deleted. We can restore it and set the is_deleted to false
            new_role.is_deleted = False
            new_role.description = request.description
            new_role.created_by = current_user
            db.commit()
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={
                "success": True,
                "msg": "Role created succesfully!"
            })
        elif new_role is not None and new_role.is_deleted == False:
            #! If the role is not deleted, we can not create it.
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                "success": False,
                "msg": "Role already exists!"
            })

        new_role = Role(
            name=request.name.lower(),
            description=request.description,
            created_on=datetime.now(),
            created_by=current_user
        )
        db.add(new_role)
        db.commit()
        db.refresh(new_role)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "success": True,
            "msg": "role created succesfully!"
        })

    @staticmethod
    def get_all_roles(
        db: Session, 
        start: Optional[int] = None, 
        limit: Optional[int] = None
    ) -> JSONResponse:
        """ Esta funcion los que hace es contar todos los registros de la base de datos,
        y paginar el listado de la informacion.

        #? ENDPOINT /roles/ GET
        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            start (int, optional): Este argumento sirve para 
            indicar el inicio de nuestro paginador. Defaults to None.
            limit (int, optional): Este argumento sirve para 
            indicar el limite de nuestro paginador. Defaults to None.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success en caso de tener exito nos mostarara la propiedad numRows con la cantidad de todos los registros y data con la informacion solicitada. 
        """

        show_roles = db.query(Role)\
            .filter_by(is_deleted=False)\
            .offset(start)\
            .limit(limit)\
            .all()
        # Sacar el numero de registros
        total = len(show_roles)

        res = {
            "success": True,
            "numRows": total,
            "data": show_roles
        }
        return jsonable_encoder(res)

    @staticmethod
    def get_one_role(
        db: Session, 
        id: UUID
    ) -> JSONResponse:
        """Este metodo lo que hace es realizar la busqueda de un registro por su id 
        en el formato UUID.
        #? ENDPOINT /roles/{id} GET

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa algo que 
            no se encuentre en este formato sera invalido.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success en caso de tener exito nos mostarara la propiedad data con la informacion del usuario buscado. 
        """
        role = db.query(Role).filter(Role.id == id)\
            .filter_by(is_deleted=False)\
            .first()
        if not role:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                "success": False,
                "msg": "Not Found"
            })

        res = {
            'success': True,
            'data': role
        }
        return jsonable_encoder(res)

    @staticmethod
    def update_role_info(
        db: Session, 
        id: UUID, 
        request: role_schemas.UpdateRole, 
        current_user: str
    ) -> JSONResponse:
        """Este metodo realiza la actualizacion de datos sobre un registro 
        filtrado por su id, se pide el current_user para tener llenados la informacion 
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
        role = db.query(Role).filter(Role.id == id)\
            .filter(Role.is_deleted == False)\
            .first()
        # Si no existe devolvemos un error
        if not role:
            # Si no lo encuentra regresamos
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "msg": "Not Found"
                })
        # Verificar si existe el role
        if request.name != role.name:
            if db.query(Role).filter(Role.name == request.name)\
                    .first():
                return JSONResponse(status_code=status.HTTP_200_OK, content={
                    "success": True,
                    "msg": "Choose Another Name!"
                })

        if request.name is None or request.name =="":
            request.name = role.name

        # Pero si lo encuentra. Actualiza!
        role.description = request.description
        role.name = request.name
        role.updated_by = current_user
        role.updated_on = datetime.now()
        db.add(role)
        db.commit()
        return JSONResponse(status_code=202, content={
            "success": True,
            "msg": "Updated successfully"
        })

    @staticmethod
    def delete_one_role(
        db: Session, 
        id: UUID
    ) -> Optional[JSONResponse]:
        """Este metodo lo que hace es eliminar un registro (soft-deleted) 
        filtrandolo por su id en formato GUID V4

        #? ENDPOINT /roles/{id}/delete/ DELETE
        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. 
            Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa
            algo que no se encuentre en este formato sera invalido.
            current_user (str): Este argumento es el ID del usuario el cual
            es un GUID se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            Optional[JSONResponse]: status code 204 NO CONTENT Esto se debe a un bug que esta tratando se arreglarse en FASTAPI y para usar 
                el método DELETE es necesario regresas NONE en nuestros métodos pero en caso de algun erro devolvemos un JSONRESPONSE. 
        """

        is_d = True
        role = db.query(Role)\
            .filter(Role.id == id)\
            .filter_by(is_deleted=False)
        if is_d == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "msg": "Its not possible!"
                })
        if not role.first():
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={
                                    "success": False,
                                    "msg": "Not Found"
                                })
        role.update({Role.is_deleted: is_d})
        db.commit()

        return None

    @staticmethod
    def show_role_with_users(
        db: Session, 
        id: UUID, 
        start: Optional[int] = None, 
        limit: Optional[int] = None
    ) -> JSONResponse:
        """Esta funcion lo que hace es filtrar un registro por su id en GUID
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
        show_role_with_users = db.query(
            Role.id,
            Role.name,
            Role.created_on,
            Users.id.label("user_id"),
            Users.email.label("user_email"),
            Users.status.label("user_status"),
            Users.created_on.label("user_created_on"),
            Users.created_by.label("user_created_by"),
        )\
            .join(Role, isouter=True)\
            .filter(Role.id == id)\
            .filter(Users.is_deleted == False)\
            .filter(Role.is_deleted == False)\
            .offset(start).limit(limit).all()

        total = len(show_role_with_users)

        res = {"success": True,
               "numRows": total,
               "data": show_role_with_users}
        return jsonable_encoder(res)

    @staticmethod
    def show_actions_and_modules(
        db: Session, 
        id: UUID, 
        start: Optional[int] = None, 
        limit: Optional[int] = None
    ) -> JSONResponse:
        """El método show_actions_and_modules lo que hace es filtrar el registro por ID y con ello nos trae 
        sus modulos asignados y el nombre de las acciones que tiene. 

        #? ENDPOINT /roles/{id}/permissions/ GET

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa algo que no se encuentre en este formato sera invalido.
            start (int, optional): Este argumento sirve para indicar el inicio de nuestro paginador. Defaults to None.
            limit (int, optional): Este argumento sirve para indicar el limite de nuestro paginador. Defaults to None.

        Returns:
            JSONResponse:  Nos devuelve una respuesta en JSON con la propiedad success
                en caso de tener exito nos mostarara la propiedad numRows con la cantidad de todos
                los registros y data con la informacion solicitada. 
        """
        permission = db.query(
            Module.name.label("module_name"),
            Actions.action_name
        ).order_by(Module.name)\
            .join(Role_Actions, isouter=False)\
            .join(Module, isouter=False)\
            .filter(Role_Actions.role_id == id)\
            .filter(Role_Actions.actions_id == Actions.id)\
            .filter(Actions.module_id == Module.id)\
            .filter(Actions.is_deleted == False)\
            .filter(Actions.value == True)\
            .filter(Module.is_deleted == False)\
            .filter(Role_Actions.is_deleted == False)\
            .offset(start)\
            .limit(limit)\
            .all()
            
        total = len(permission)

        res = {
            "success": True,
            "numRows": total,
            "data": permission
        }
        return jsonable_encoder(res)

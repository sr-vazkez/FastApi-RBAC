from datetime import datetime
from typing import Dict, Optional
from uuid import UUID


from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.schemas import action_schemas
from app.models.module import Module
from app.models.actions import Actions

class ActionsOperations():
    @staticmethod
    def create_new_action(
        db: Session, 
        current_user: str, 
        request: action_schemas.ActionCreate
    ) -> JSONResponse:
        """Este metodo lo que hace es crear una accion, 
        se pide el current_user para tener llenados
        la informacion para los datos de auditoria. 

        #? Endpoint /actions/create POST

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            current_user (str): Este argumento es el ID del usuario el cual es un GUID
             se obtiene con la clase Authorize y el metodo get_jwt_subject()
            request (Pydantic model): Modelo de pydantic para recibir la informacion proporcionada
             por el frontend o el usuario.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success y la propiedad msg
             con sus respectivos valores. En caso contrario nos mostrara la propiedad success 
             y la propiedad msg.
        """

        new_action = db.query(Actions
        ).filter(
            Actions.module_id == request.module_id,
            Actions.action_name == request.action_name.lower()
        )\
            .first()

        #print(50*'-')
        #print(new_action)
        #print(50*'-')

        check_module = db.query(Module.id).filter(
            Module.id == request.module_id
            )\
            .filter(Module.is_deleted == False).first()

        #print(50*'-')
        #print(check_module)
        #print(50*'-')
        
        if new_action and new_action.is_deleted == True:
                #! If the action is deleted, we can restore it and set the is_deleted to False.
                #print("If the action is deleted, we can restore it.")
                new_action.is_deleted = False
                new_action.created_on = datetime.now()
                new_action.created_by = current_user
                db.commit()
                return JSONResponse(status_code=status.HTTP_201_CREATED, content={
                    "success": True,
                    "msg": "Action created succesfully!"
                })
        
        
        elif new_action is not None and new_action.is_deleted == False:
                #! If the user is not deleted, we can not create it.
                #print("If the user is not deleted, we can not create it.")
                return JSONResponse(status_code=status.HTTP_200_OK, content={
                    "success": True,
                    "msg": "Action already exists!"
                })

        elif not check_module:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                    "success": False,
                    "msg": "Invalid Module!"
                })

        new_action = Actions(
            action_name=request.action_name,
            description = request.description,
            value=request.value,
            module_id=request.module_id,
            created_on=datetime.now(),
            created_by=current_user
        )
        db.add(new_action)
        db.commit()
        db.refresh(new_action)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "success": True,
            "msg": "Actions created succesfully!"
        })

    @staticmethod
    def get_all_actions(
        db: Session, 
        start:Optional[int] = None, 
        limit:Optional[int] = None
    ) -> JSONResponse:
        """ Esta funcion los que hace es contar todos los registros de la base de datos,
        y paginar el listado de la informacion.

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
        show_roles = db.query(
            Actions.id,
            Actions.action_name,
            Actions.value,
            Actions.created_on,
            Actions.module_id,
            Module.name.label("module_name"),
            Module.created_on.label("module_created_on")
            )\
            .join(Module, isouter=True)\
            .filter(Actions.is_deleted==False)\
            .filter(Module.is_deleted == False)\
            .offset(start)\
            .limit(limit)\
            .all()
        # Sacar el numero de registros
        total = db.query(Actions)\
            .filter_by(is_deleted=False)\
            .count()
        
        res = {
            "success": True,
            "numRows": total,
            "data": show_roles
        }
        return jsonable_encoder(res)

    @staticmethod
    def get_one_action(
        db: Session,
        id: UUID
    ) -> JSONResponse:
        """Este metodo lo que hace es realizar la busqueda de un registro por su id en el formato UUID.
        #? ENDPOINT /actions/{id} GET
        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa algo que 
            no se encuentre en este formato sera invalido.

        Returns:
            JSONResponse:  Nos devuelve una respuesta en JSON con la propiedad success
                en caso de tener exito nos mostarara la propiedad data con la informacion de la accion solicitada. 
        """

        action = db.query(
            Actions.id,
            Actions.action_name,
            Actions.value,
            Actions.created_on,
            Actions.module_id,
            Module.name.label("module_name"),
            Module.created_on.label("module_created_on")
            )\
            .join(Module, isouter=True)\
            .filter(Actions.id == id)\
            .filter(Actions.is_deleted==False)\
            .filter(Module.is_deleted == False)\
            .first()

        if not action:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                "success": False,
                "msg": "Not Found"
            })
        res = {
                "success": True,
                "data": action
            }
        return jsonable_encoder(res)

    @staticmethod
    def update_action_info(
        db: Session,
        id: UUID, 
        request: action_schemas.UpdateAction , 
        current_user:str
    ) -> JSONResponse:
        """Este metodo realiza la actualizacion de datos sobre un registro 
        filtrado por su id, se pide el current_user para tener llenados la informacion 
        para los datos de auditoria. 

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
        #! Buscamos a un user por su id, este no debe de estar marcado como eliminado
        #? Buscamos la accion de un modulo el cual es filtrado por un id
            #! Si es que el usuario quiso no mandar el action_name lo dejamos por el actual

        action = db.query(Actions)\
            .filter(Actions.id == id)\
            .filter(Actions.is_deleted==False)\
            .first()        
        #! Si no lo encuentra regresamos un error
        if not action:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={
                    "success": False,
                    "msg": "Not Found"
                })

        check_action_module = db.query(Actions.action_name)\
            .filter(Actions.module_id == action.module_id)\
            .filter(Actions.is_deleted == False)\
            .all()
        #! verificamos que si el action_name no esta vacio        
        if request.action_name is not None:  
            request.action_name.lower()
            for i in check_action_module:
                #! Recorremos el query para poder comparara
                for name_action in i:
                    #! but es sqlalchemy hay que hacer doble for para que sea string
                    if request.action_name == name_action:
                        #! Si el request es al primer elemento regresamos que ya existe esa accion :D
                        return JSONResponse(status_code=status.HTTP_200_OK, content={
                            "success": True,
                            "msg": "Action already exists!"
                        })
                        break 
        #! Si es que el usuario quiso no mandar el action_name lo dejamos por el actual
        if request.action_name is None or request.action_name == "":
            request.action_name = action.action_name 

        #! Actualiza!
        action.action_name = request.action_name
        action.description = request.description
        action.value = request.value 
        action.updated_by = current_user
        action.updated_on = datetime.now()
        db.add(action)
        db.commit()
        db.refresh(action)
        return JSONResponse(status_code=202, content={
            "success": True,
            "msg": "Updated successfully"
            })

    @staticmethod
    def delete_one_action(
        db: Session,
        id: UUID
    ) -> Optional[JSONResponse]:
        """Este metodo lo que hace es eliminar un registro (soft-deleted) 
        filtrandolo por su id en formato GUID V4

        #? ENDPOINT /actions/{id}/delete/ DELETE
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
        role = db.query(Actions)\
            .filter(Actions.id == id)\
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
        role.update({Actions.is_deleted: is_d, Actions.value: False})
        db.commit()

        return None
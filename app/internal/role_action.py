from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import status
#from app.models.users import Users
from app.models.role_actions import Role_Actions
from app.models.actions import Actions
from app.models.roles import Role
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.schemas import role_actions_schemas

class RoleActions():
    @staticmethod
    def show_all_actions_assigned(
        db:Session, 
        start: Optional[int] = None, 
        limit: Optional[int]=None
    ) -> JSONResponse:
        """Esta funcion los que hace es contar todos los registros de la base de datos,
        y paginar el listado de la informacion.

        #? ENDPOINT /role-actions/ GET

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            start (int, optional): Este argumento sirve para 
            indicar el inicio de nuestro paginador. Defaults to None.
            limit (int, optional): Este argumento sirve para 
            indicar el limite de nuestro paginador. Defaults to None.

        Returns:
            JSONResponse:Nos devuelve una respuesta en JSON con la propiedad success
            en caso de tener exito nos mostarara la propiedad numRows con la cantidad de todos
            los registros y data con la informacion solicitada. 
        
        """  
        actions = db.query(
        Role_Actions.id,
        Role_Actions.actions_id,
        Role_Actions.role_id,
        Role_Actions.description,
        Role_Actions.created_on
        ).filter(Role_Actions.is_deleted==False)\
        .offset(start)\
        .limit(limit)\
        .all()
        
        total = len(actions)
        res = {"success": True,"numRows": total,"data": actions}
        return jsonable_encoder(res)


    @staticmethod
    def show_one_role_action(
        db: Session,
        id: UUID
    ) -> JSONResponse:
        """Este metodo lo que hace es realizar la busqueda de un registro por su id 
        en el formato UUID.

        #? ENDPOINT /role-actions/{id}

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa algo que 
            no se encuentre en este formato sera invalido.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
                en caso de tener exito nos mostarara la propiedad data con la informacion del usuario buscado. 
        """
        action = db.query(
            Role_Actions.id,
            Role_Actions.actions_id,
            Role_Actions.role_id,
            Role_Actions.description,
            Role_Actions.created_on
        )\
        .filter(Role_Actions.id == id)\
        .filter(Role_Actions.is_deleted==False).first()

        res = {
            'success':True,
            'data':action
        }
        return jsonable_encoder(res)

    
    @staticmethod
    def assing_role_and_actions(
        db: Session, 
        request: role_actions_schemas.assigned_action,
        current_user: str
    ):
        """Asignar una accion a un rol. Esta funcion lo que hace es
        asignar acciones a un rol 

        #? ENPOINT /role-actions/assing/actions
        
        Args:
            request (role_actions_schemas.assigned_action):Schema con ID rol y ID action 
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success y la propiedad msg
            con sus respectivos valores. En caso contrario nos mostrara la propiedad success 
            y la propiedad msg.
        """
        check_status = db.query(Role_Actions)\
        .filter(Role_Actions.role_id == request.role_id)\
        .filter(Role_Actions.actions_id == request.actions_id)\

        if check_status.filter(Role_Actions.is_deleted == False).first():
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                "success": True,
                "msg": "It was already assign"
                })

        if check_status.filter(Role_Actions.is_deleted == True).first():
            is_d = False
            check_status.update({
                **request.dict(),
                "is_deleted": is_d,
                "updated_by":current_user
            })
            db.commit()
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={
                'success':True,
                "message": "Action assign in a Role"
                })
    
        else:
            check_role = db.query(Role).filter(Role.id == request.role_id)\
                .filter(Role.is_deleted == False).first()
            if not check_role:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                        "success": False,
                        "msg": "Invalid role!"
                    })

            check_action = db.query(Actions).filter(Actions.id == request.actions_id)\
                .filter(Actions.is_deleted == False).first()

            if not check_action:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                        "success": False,
                        "msg": "Invalid action!"
                    })
            assing_action = Role_Actions(**request.dict(), created_by=current_user)
            db.add(assing_action)
            db.commit()
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={
                'success':True,
                "message": "Action assign in a Role"
                })


    @staticmethod
    def deleted_assing_role_and_actions(
        db:Session,
        id: UUID,
        current_user:str
    ) -> Optional[JSONResponse]:
        """Este metodo lo que hace es eliminar un registro (soft-deleted) 
        filtrandolo por su id en formato GUID V4

        #? ENDPOINT /role-actions/{id} DELETED

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. 
            Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa
            algo que no se encuentre en este formato sera invalido.
            current_user (str): Este argumento es el ID del usuario el cual
            es un GUID se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            Optional[JSONResponse]:status code 204 NO CONTENT Esto se debe a un bug que esta tratando se arreglarse en FASTAPI y para usar 
            el método DELETE es necesario regresas NONE en nuestros métodos pero en caso de algun erro devolvemos un JSONRESPONSE. 
        """
        is_d = True
        role_action = db.query(Role_Actions).filter(
            Role_Actions.id == id).\
            filter(Role_Actions.is_deleted == False)
        if not role_action.first():
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                "success":True,
                "msg": "Not Found"
                })

        role_action.update({
            "is_deleted": is_d,
            "updated_by": current_user
        })
        db.commit()
        return None
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.schemas import user_schemas
from app.internal.hashing import Hash
from app.models.users import Users
from app.models.roles import Role


class UsersActions():
    @staticmethod
    def current_user_profile(
        db: Session,
        current_user: str
    ) -> JSONResponse:
        """Este metodo lo que hace es mostrar la informacion del usuario en session, 
        incluyendo informacion sobre el role que tiene.
        #? Endpoint /users/profile GET
        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            current_user (str): Este argumento es el ID del usuario el cual es un GUID 
            se obtiene con la clase Authorize y el metodo get_jwt_subject()
        Returns:
            JSONResponse:  Nos devuelve una respuesta en JSON con la propiedad success
                en caso de tener exito nos mostarara la propiedad data con la informacion del 
                usuario en session. En caso contrario nos mostrara la propiedad success y 
                la propiedad msg.
        """
        #! We need to validate if the user and the role exist
        user = db.query(
            Users.id,
            Users.email,
            Users.status,
            Users.created_on,
            Users.role_id,
            Role.name.label("role_name"),
            Role.created_on.label("role_created_on")
        )\
            .join(Role, isouter=True)\
            .filter(Users.id == current_user)\
            .filter(Users.is_deleted == False)\
            .filter(Role.is_deleted == False)\
            .first()

        #! if the user and the role exist we return the user and the role with the information

        if not user:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                "success": False,
                "msg": "Invalid User!"
            })

        res = {
            "success": True,
            "data": user
        }
        return jsonable_encoder(res)

    @staticmethod
    def create_new_user(
        db: Session,
        current_user: str,
        request: user_schemas.UserCreate
    ) -> JSONResponse:
        """Este metodo lo que hace es crear un usuario, 
        se pide el current_user para tener llenados
        la informacion para los datos de auditoria. 

        #? Endpoint /users/create POST

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
        new_user = db.query(Users).filter(Users.email == request.email)\
            .first()
        check_role = db.query(Role.id).filter(Role.id == request.role_id)\
            .filter(Role.is_deleted == False).first()

        if new_user is not None and new_user.is_deleted == True:
            #! If the user is deleted, we can restore it and set the is_deleted to False and update Password.
            #print("If the user is deleted, we can restore it.")
            new_user.is_deleted = False
            new_user.password = Hash.bcrypt(request.password)
            new_user.created_on = datetime.now()
            new_user.created_by = current_user
            db.commit()
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={
                "success": True,
                "msg": "User created succesfully!"
            })
        elif new_user is not None and new_user.is_deleted == False:
            #! If the user is not deleted, we can not create it.
            #print("If the user is not deleted, we can not create it.")
            return JSONResponse(status_code=status.HTTP_200_OK, content={
                "success": True,
                "msg": "User already exists!"
            })
        #! If the user is not in the database, we can create it.
        #print("If the user is not in the database, we can create it.")
        #! Validar que el request.role_id exista en la base de datos
        elif not check_role:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
                "success": False,
                "msg": "Invalid role!"
            })

        new_user = Users(
            email=request.email,
            password=Hash.bcrypt(request.password),
            role_id=request.role_id,
            created_on=datetime.now(),
            created_by=current_user
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "success": True,
            "msg": "User created succesfully!"
        })

    @staticmethod
    def get_all_users(
        db: Session,
        start: Optional[int] = None,
        limit: Optional[int] = None
    ) -> JSONResponse:
        """Esta funcion los que hace es contar todos los registros de la base de datos,
        y paginar el listado de la informacion.

        #? ENDPOINT /users/ GET
        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            start (int, optional): Este argumento sirve para 
            indicar el inicio de nuestro paginador. Defaults to None.
            limit (int, optional): Este argumento sirve para 
            indicar el limite de nuestro paginador. Defaults to None.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
                en caso de tener exito nos mostarara la propiedad numRows con la cantidad de todos
                los registros y data con la informacion solicitada. 
        """
        show_users = db.query(
            Users.id,
            Users.email,
            Users.status,
            Users.created_on,
            Users.role_id,
            Role.name.label("role_name"),
            Role.created_on.label("role_created_on")
        )\
            .join(Role, isouter=True)\
            .filter(Users.is_deleted == False)\
            .filter(Role.is_deleted == False)\
            .offset(start).limit(limit).all()

        total = len(show_users)
        
        res = {"success": True,
               "numRows": total,
               "data": show_users}
        return jsonable_encoder(res)

    @staticmethod
    def get_one_user(
        db: Session,
        id: UUID
    ) -> JSONResponse:
        """Este metodo lo que hace es realizar la busqueda de un registro por su id 
        en el formato UUID.

        #? ENDPOINT /users/{id} GET
        
        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa algo que 
            no se encuentre en este formato sera invalido.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
                en caso de tener exito nos mostarara la propiedad data con la informacion del usuario buscado. 
        """

        user = db.query(
            Users.id,
            Users.email,
            Users.status,
            Users.created_on,
            Users.role_id,
            Role.name.label("role_name"),
            Role.created_on.label("role_created_on"))\
            .join(Role, isouter=True)\
            .filter(Users.id == id)\
            .filter(Users.is_deleted == False)\
            .filter(Role.is_deleted == False)\
            .first()
        if not user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                "success": False,
                "msg": "Not Found"
            })

        res = {
            "success": True,
            "data": user
        }

        return jsonable_encoder(res)

    @staticmethod
    def update_user_info(
        db: Session,
        id: UUID,
        request: user_schemas.UpdateUser,
        current_user: str
    ) -> JSONResponse:
        """Este metodo realiza la actualizacion de datos sobre un registro 
        filtrado por su id, se pide el current_user para tener llenados la informacion 
        para los datos de auditoria. 

        #? ENDPOINT /users/{id} PUT

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
        user = db.query(Users).filter(Users.id == id)\
            .filter_by(is_deleted=False)\
            .first()
        #! Si no existe el user, devolvemos un error
        if not user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                "success": False,
                "msg": "Not Found"
            })
        #! We need validate if the email is unique
        if request.email != user.email:
            if db.query(Users).filter(Users.email == request.email)\
                    .first():
                return JSONResponse(status_code=status.HTTP_200_OK, content={
                    "success": True,
                    "msg": "Email was taken!"
                })
        #! We need validate if the email request is none or empty string set the email to the current email
        if request.email is None or request.email == "":
            request.email = user.email

        #! Pero si lo encuentra. Actualiza!
        user.status = request.status
        user.email = request.email
        user.updated_by = current_user
        user.updated_on = datetime.now()
        db.add(user)
        db.commit()
        return JSONResponse(status_code=202, content={
            "success": True,
            "msg": "Updated successfully",
        })

    @staticmethod
    def delete_one_user(
        db: Session,
        id: UUID,
        current_user: str
    ) -> Optional[JSONResponse]:
        """Este metodo lo que hace es eliminar un registro (soft-deleted) 
        filtrandolo por su id en formato GUID V4

        #? ENDPOINT /users/{id}/delete/ DELETE
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
        user = db.query(Users)\
            .filter(Users.id == id)\
            .filter_by(is_deleted=False)
        if is_d == False:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "msg": "Its not possible!"
                })
        if current_user == id:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "msg": "You can not deleted your self!!"
                })

        if not user.first():
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={
                                    "success": False,
                                    "msg": "Not Found"
                                })
        user.update({Users.is_deleted: is_d, Users.status: False})
        db.commit()

        return None

    @staticmethod
    def update_password_user(
        db: Session,
        id: UUID,
        request: user_schemas.UpdatePass,
        current_user: str
    ) -> JSONResponse:
        """Este metodo lo que hace es actualizar el campo del password de usuario
        filtrandolo por su id en formato UUID v4. Se pide el current_user para evitar
        que el usuario actualize su propio password usando esta funcion y endpoint.

        #? ENDPOINT /users/{id}/update/passwords PATCH

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY.
            Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa
            algo que no se encuentre en este formato sera invalido.
            request (Pydantic model): Modelo de pydantic para recibir 
            la informacion proporcionada por el frontend o el usuario.
            current_user (str): Este argumento es el ID del usuario el
            cual es un GUID se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success 
            y la propiedad msg con sus respectivos valores.
            En caso contrario nos mostrara la propiedad success y la propiedad msg.
        """
        #! We need validate if the user exist
        user = db.query(Users).filter(Users.id == id)\
            .filter_by(is_deleted=False)
        #! If the user is a current user, return error
        if current_user == id:
            return JSONResponse(status_code=status. HTTP_200_OK, content={
                "success": True,
                "msg": "You can not update your password!!"
            })
        if not user.first():
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                "success": False,
                "msg": "Not Found"
            })

        request.new_password = Hash.bcrypt(request.new_password)
        user.update({Users.password: request.new_password})
        db.commit()
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={
            "success": True,
            "msg": "Updated password successfully"
        })

    @staticmethod
    def update_my_password(
        db: Session,
        request: user_schemas.UpdatePassMe,
        current_user: str
    ) -> JSONResponse:
        """Este metodo lo que hace es actualizar el campo del password
        del usuario en session. Como medida de seguridad se pide el password actual. 
        Asi mismo se pide que se confirme el password nuevo.

        #? ENDPOINT /users/profile/update/password PATCH

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. 
            Defaults to Depends().
            request (Pydantic model): Modelo de pydantic para recibir la informacion 
            proporcionada por el frontend o el usuario.
            current_user (str): Este argumento es el ID del usuario el cual es un GUID,
            se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success 
            y la propiedad msg con sus respectivos valores. En caso contrario nos mostrara 
            la propiedad success y la propiedad msg.
        """
        user = db.query(Users).filter(Users.id == current_user)\
            .filter_by(is_deleted=False).first()
        if not user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                "success": False,
                "msg": "Not Found"
            })
        if not Hash.verify(user.password, request.actual_password):
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
                "success": False,
                "msg": "Invalid Credentials"
            })
        user.password = Hash.bcrypt(request.new_password)
        user.updated_by = current_user
        user.updated_on = datetime.now()
        db.add(user)
        db.commit()
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={
            "success": True,
            "msg": "Updated password successfully"
        })

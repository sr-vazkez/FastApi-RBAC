from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.sql.expression import false
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app import main
from app.schemas import user_schemas
from app.extras.hashing import Hash
from app.models.users import Users
from app.models.roles import Role

extra = {"event.category": "app_log"}


class UsersActions:
    """Esta clase realiza operacions en usuarios.

    Podemos crear, actualizar ,eliminar y editar ademas de
     generar otras acciones adiciionales.
    """

    def __init__(
        self,
        db: Optional[Session] = None,
        request: Optional[user_schemas.UserCreate] = None,
        current_user: Optional[str] = None,
        start: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> None:
        self.db: Optional[Session] = db
        self.request: Optional[user_schemas.UserCreate] = request
        self.current_user: Optional[str] = current_user
        self.start: Optional[int] = start
        self.limit: Optional[int] = limit

    def current_user_profile(self, db: Session, current_user: str) -> JSONResponse:
        """Este metodo lo que hace es mostrar la informacion del usuario en session.

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
        #  We need to validate if the user and the role exist
        user = (
            db.query(
                Users.id,
                Users.email,
                Users.is_active,
                Users.role_id,
                Role.name.label("role_name"),
            )
            .join(Role, isouter=True)
            .filter(Users.id == current_user)
            .filter(Users.is_deleted == false())
            .filter(Role.is_deleted == false())
            .first()
        )

        # if the user and the role exist we return the user and the role with the information

        if not user:
            main.logger.info(msg="Invalid User", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "Invalid User!"},
            )

        res = {"success": True, "data": user}
        return jsonable_encoder(res)

    def create_new_user(
        self, db: Session, current_user: str, request: user_schemas.UserCreate
    ) -> JSONResponse:
        """Este metodo lo que hace es crear un usuario.

        Se pide el current_user para tener llenados la informacion para los datos de auditoria.

        #? Endpoint /users/create POST

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            current_user (str): Este argumento es el ID del usuario el cual es un GUID
             se obtiene con la clase Authorize y el metodo get_jwt_subject()
            request (Pydantic model): Modelo de pydantic para recibir la informacion proporcionada
             por el frontend o el usuario.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success
             y la propiedad msg con sus respectivos valores.
             En caso contrario nos mostrara la propiedad success y la propiedad msg.
        """
        new_user = db.query(Users).filter(Users.email == request.email).first()
        check_role = (
            db.query(Role.id)
            .filter(Role.id == request.role_id)
            .filter(Role.is_deleted == false())
            .first()
        )
        if not check_role:
            main.logger.info(msg="Invalid role!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "Invalid role!"},
            )

        if new_user is not None and new_user.is_deleted is True:
            # If the user is deleted, we can restore it and
            # set the is_deleted to False and update Password.
            # print("If the user is deleted, we can restore it.")
            new_user.is_deleted = False
            new_user.role_id = request.role_id
            new_user.password = Hash().bcrypt(request.password)
            new_user.created_on = datetime.now()
            new_user.created_by = current_user
            db.commit()
            main.logger.info(msg="User created succesfully!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"success": True, "msg": "User created succesfully!"},
            )
        elif new_user is not None and new_user.is_deleted is False:
            # If the user is not deleted, we can not create it.
            # print("If the user is not deleted, we can not create it.")
            main.logger.info(msg="User already exists!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"success": True, "msg": "User already exists!"},
            )
        new_user = Users(
            email=request.email,
            password=Hash().bcrypt(request.password),
            role_id=request.role_id,
            created_on=datetime.now(),
            created_by=current_user,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        main.logger.info(msg="User created succesfully!", extra=extra)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"success": True, "msg": "User created succesfully!"},
        )

    def get_all_users(
        self,
        db: Session,
        current_user: str,
        start: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> JSONResponse:
        """Este metodo cuenta todos los registros y paginar el listado de la informacion.

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
        show_users = (
            db.query(
                Users.id,
                Users.email,
                Users.is_active,
                Users.role_id,
                Role.name.label("role_name"),
            )
            .join(Role, isouter=True)
            .filter(Role.name != "super admin")
            .filter(Users.id != current_user)
            .filter(Users.is_deleted == false())
            .filter(Role.is_deleted == false())
            .offset(start)
            .limit(limit)
            .all()
        )

        total = len(show_users)
        main.logger.info(msg="List of Users is display!", extra=extra)
        res = {"success": True, "numRows": total, "data": show_users}
        return jsonable_encoder(res)

    def get_one_user(self, db: Session, id: UUID) -> JSONResponse:
        """Realizar la busqueda de un registro por su id.

        #? ENDPOINT /users/{id} GET

        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY. Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa algo que
            no se encuentre en este formato sera invalido.

        Returns:
            JSONResponse: Nos devuelve una respuesta en JSON con la propiedad success en
             caso de tener exito nos mostarara la propiedad data con la informacion del usuario.
        """
        user = (
            db.query(
                Users.id,
                Users.email,
                Users.is_active,
                Users.role_id,
                Role.name.label("role_name"),
            )
            .join(Role, isouter=True)
            .filter(Users.id == id)
            .filter(Role.name != "super admin")
            .filter(Users.is_deleted == false())
            .filter(Role.is_deleted == false())
            .first()
        )
        if not user:
            main.logger.info(msg=f"User {id} not found!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )

        res = {"success": True, "data": user}
        main.logger.info(msg=f"User {id} is found!", extra=extra)
        return jsonable_encoder(res)

    def update_user_info(
        self,
        db: Session,
        id: UUID,
        request: user_schemas.UpdateUser,
        current_user: str,
    ) -> JSONResponse:
        """Este metodo realiza la actualizacion de datos sobre un registro.

        Filtrado por su id, se pide el current_user para tener llenados la informacion
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
        # Buscamos a un user por su id, este no debe de estar marcado como eliminado
        user = (
            db.query(Users).filter(Users.id == id).filter_by(is_deleted=False).first()
        )
        # Si no existe el user, devolvemos un error
        if not user:
            main.logger.info(msg=f"User {id} not found!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )

        # Ahora se tiene que validar que exista el request.role_id
        role_search = (
            db.query(Role)
            .filter(Role.id == request.role_id)
            .filter(Role.is_deleted == false())
            .first()
        )
        if not role_search:
            main.logger.info(msg=f"Role {request.role_id} is not valid!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Insert a valid Role"},
            )

        # We need validate if the email is unique
        if request.email != user.email:
            if db.query(Users).filter(Users.email == request.email).first():
                main.logger.info(msg=f"{request.email} was taken!", extra=extra)
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"success": True, "msg": "Email was taken!"},
                )
        # We need validate if the email request is none or empty string
        # set the email to the current email
        if request.email is None or request.email == "":
            request.email = user.email

        # Pero si lo encuentra. Actualiza!
        user.role_id = request.role_id
        user.is_active = request.is_active
        user.email = request.email
        user.updated_by = current_user
        user.updated_on = datetime.now()
        db.add(user)
        db.commit()
        main.logger.info(msg=f"User {id} is updated!", extra=extra)
        return JSONResponse(
            status_code=202,
            content={
                "success": True,
                "msg": "Updated successfully",
            },
        )

    def delete_one_user(
        self, db: Session, id: UUID, current_user: str
    ) -> Optional[JSONResponse]:
        """Este metodo lo que hace es eliminar un registro (soft-deleted).

        Filtrandolo por su id en formato GUID V4

        #? ENDPOINT /users/{id}/delete/ DELETE
        Args:
            db (Session): Session para realizar acciones con SQLALCHEMY.
            Defaults to Depends().
            id (UUID v4): Este argumento es del tipo UUID v4 si se ingresa
            algo que no se encuentre en este formato sera invalido.
            current_user (str): Este argumento es el ID del usuario el cual
            es un GUID se obtiene con la clase Authorize y el metodo get_jwt_subject()

        Returns:
            Optional[JSONResponse]: status code 204 NO CONTENT para usar el método DELETE
             es necesario regresas NONE en caso de algun erro devolvemos un JSONRESPONSE.
        """
        is_d = True

        user = db.query(Users).filter(Users.id == id).filter_by(is_deleted=False)

        if is_d is False:
            main.logger.info(
                msg="value is true but something was changed to false!", extra=extra
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": False, "msg": "Its not possible!"},
            )

        if current_user == id.__str__():
            main.logger.info(
                msg=f"User {id} was trying to delete its self!", extra=extra
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"msg": "You can not deleted your self!!"},
            )

        if not user.first():
            main.logger.info(msg=f"User {id} not found", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )

        user.update({Users.is_deleted: is_d, Users.is_active: False})
        db.commit()
        main.logger.info(msg=f"User {id} it's deleted!", extra=extra)
        return None

    def update_password_user(
        self,
        db: Session,
        id: UUID,
        request: user_schemas.UpdatePass,
        current_user: str,
    ) -> JSONResponse:
        """Este metodo lo que hace es actualizar el campo del password de usuario.

        Filtrandolo por su id en formato UUID v4. Se pide el current_user para evitar
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
        # We need validate if the user exist
        user = db.query(Users).filter(Users.id == id).filter_by(is_deleted=False)

        # If the user is a current user, return error
        if current_user == id.__str__():
            main.logger.info(
                msg=f"User {id} cannot update self password in this endpoint!",
                extra=extra,
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"success": True, "msg": "You can not update your password!!"},
            )

        if not user.first():
            main.logger.info(msg=f"User {id} not found!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )

        request.new_password = Hash().bcrypt(request.new_password)
        user.update({Users.password: request.new_password})
        db.commit()
        main.logger.info(
            msg=f"the password from user {id} updated successfully!", extra=extra
        )
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={"success": True, "msg": "Updated password successfully"},
        )

    def update_my_password(
        self, db: Session, request: user_schemas.UpdatePassMe, current_user: str
    ) -> JSONResponse:
        """Actualiza el campo del password del usuario en session.

        Como medida de seguridad se pide el password actual.
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
        user = (
            db.query(Users)
            .filter(Users.id == current_user)
            .filter_by(is_deleted=False)
            .first()
        )
        if not user:
            main.logger.info(msg=f"User {current_user} not found!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Not Found"},
            )
        if not Hash().verify(user.password, request.actual_password):
            main.logger.info(msg="Invalid credentials!", extra=extra)
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "msg": "Invalid Credentials"},
            )
        user.password = Hash().bcrypt(request.new_password)
        user.updated_by = current_user
        user.updated_on = datetime.now()
        db.add(user)
        db.commit()
        main.logger.info(
            msg=f"the password from current user {id} updated successfully!",
            extra=extra,
        )
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={"success": True, "msg": "Updated password successfully"},
        )

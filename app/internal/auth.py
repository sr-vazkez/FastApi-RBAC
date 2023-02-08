import datetime

from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from fastapi_another_jwt_auth import AuthJWT

from app.models import Users
from app.models.actions import Actions
from app.models.module import Module
from app.models.role_actions import Role_Actions
from app.models.roles import Role
from app.schemas import schemas_config
from app.extras.hashing import Hash
from app.dependencies.data_conexion import get_db


class AuthActions():
    @staticmethod
    def user_login(
        request: schemas_config.Login,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()
    ) -> JSONResponse:
        """
        user_login Este metodo lo que realizara es la creacion del JWT Token agregando dentro de el informacion,
            con sus roles y permisos. Esto filtrando que en realidad exista el usuario en la BD.

        #? Endpoint /auth/singing POST

        Args:
            request (schemas_config.Login): Esquema con el cual hacemos un request el cual nos pide el email y el password. 
            db (Session): Sesion de SQLAlchemy para poder realizar consultas  la BD. Defaults to Depends(get_db).
            Authorize (AuthJWT, optional): Dependecia y metodo de la clase FastAPI_users, para generar nuestro token. Defaults to Depends().

        Returns:
            JSONResponse: Nos devuelve un JSON con la propiedad success y otro objeto llamado data con el access_token y el refresh_token.

        """
        try:
            user = db.query(
                Users.id,
                Users.email,
                Users.role_id,
                Users.status,
                Users.password,
                Users.is_deleted,
                Role.name.label('role_name')
            )\
                .join(Role)\
                .filter(Users.email == request.email)\
                .filter(Users.status == True)\
                .filter_by(is_deleted=False)\
                .first()

            if not user:
                return JSONResponse(
                    status_code=400, content={
                        "success": False,
                        "msg": "Invalid Credentials"
                    }
                )

            result_permission = db.query(
                Module.name,
                Actions.action_name
            ).order_by(Module.name)\
                .join(Role_Actions, isouter=False)\
                .join(Module, isouter=False)\
                .filter(Role_Actions.role_id == user.role_id.__str__())\
                .filter(Role_Actions.actions_id == Actions.id)\
                .filter(Actions.module_id == Module.id)\
                .filter(Actions.is_deleted == False)\
                .filter(Actions.value == True)\
                .filter(Module.is_deleted == False)\
                .filter(Role_Actions.is_deleted == False)\
                .all()

            permissions = {}

            for permission, action in result_permission:
                #print(permission, action)
                if permission not in permissions:
                    permissions[permission] = []

                if action not in permissions[permission]:
                    permissions[permission].append(action)

            if not Hash.verify(user.password, request.password):
                return JSONResponse(
                    status_code=400, content={
                        "success": False,
                        "msg": "Invalid Credentials"
                    })

            if user.is_deleted == True:
                return JSONResponse(
                    status_code=400, content={
                        "success": False,
                        "msg": "Invalid Credentials"
                    })

            if user.status == False:
                return JSONResponse(
                    status_code=400, content={
                        "success": False,
                        "msg": "Invalid Credentials"
                    })
            expires = datetime.timedelta(hours=2)
            expires_fresh = datetime.timedelta(hours=4)
            #! We need to convert user.id to string to be able to use it as a subject 

            another_claims = {
                "role": user.role_id.__str__(),
                "email": user.email,
                "status": user.status,
                "role_name": user.role_name,
                "permissions": permissions
            }
            access_token = Authorize.create_access_token(
                subject=user.id.__str__(), user_claims=another_claims, expires_time=expires)
            refresh_token = Authorize.create_refresh_token(
                subject=user.id.__str__(), user_claims=another_claims, expires_time=expires_fresh)

            res = {
                "success": True,
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            }
            return JSONResponse(res)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    'success': False,
                    'msg': 'Bad Request'
                })

    @staticmethod
    def refresh_token(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()
    ) -> JSONResponse:
        """ 
        Método refresh_token. Este método lo que hace es generar un refresh token para asi obtener un nuevo access token en
            caso de que nuestra session haya caducado. 

        #? Endpoint /auth/refresh GET

        Args:
            db (Session): Sesion de SQLAlchemy para poder realizar consultas  la BD. Defaults to Depends(get_db).
            Authorize (AuthJWT, optional): Dependecia y metodo de la clase FastAPI_users, para generar nuestro token. Defaults to Depends().

        Return
            JSONResponse:  Nos devuelve una respuesta en JSON con la propiedad success
                en caso de tener exito nos mostarara nuestros nuevos tokens. En caso contrario lo único que hara 
                sera regresarnos un JSON con la propiedad success y msg.
        """

        try:
            Authorize.jwt_refresh_token_required()
            current_user = Authorize.get_jwt_subject()

            if not current_user:
                    return JSONResponse(status_code=status.HTTP_421_MISDIRECTED_REQUEST, content={
                        "success": True,
                        "msg": "Could not refresh access token!"
                    })

            validate_current_user = db.query(Users).filter(
                    Users.id == current_user).first()

            if not validate_current_user or validate_current_user is None:
                    return JSONResponse(
                        status_code=421, content={
                            "success": False,
                            "msg": "The user belonging to this token no logger exist"
                        }
                    )

            """
            The jwt_refresh_token_required() function insures a valid refresh
            token is present in the request before running any code below that function.
            we can use the get_jwt_subject() function to get the subject of the refresh
            token, and use the create_access_token() function again to make a new access token
            """
            result_permission = db.query(
                    Module.name,
                    Actions.action_name
                ).order_by(Module.name)\
                    .join(Role_Actions, isouter=False)\
                    .join(Module, isouter=False)\
                    .filter(Role_Actions.role_id == validate_current_user.role_id.__str__())\
                    .filter(Role_Actions.actions_id == Actions.id)\
                    .filter(Actions.module_id == Module.id)\
                    .filter(Actions.is_deleted == False)\
                    .filter(Actions.value == True)\
                    .filter(Module.is_deleted == False)\
                    .filter(Role_Actions.is_deleted == False)\
                    .all()

            permissions = {}

            for permission, action in result_permission:
                    #print(permission, action)
                    if permission not in permissions:
                        permissions[permission] = []

                    if action not in permissions[permission]:
                        permissions[permission].append(action)
            
            expires = datetime.timedelta(hours=2)
            expires_fresh = datetime.timedelta(hours=4)

            another_claims = {
                    "role": validate_current_user.role_id.__str__(),
                    "email": validate_current_user.email,
                    "status": validate_current_user.status,
                    "permissions": permissions
                }
            new_access_token = Authorize.create_access_token(
                    subject=validate_current_user.id.__str__(), user_claims=another_claims, expires_time=expires)
            new_refresh_token = Authorize.create_refresh_token(
                    subject=validate_current_user.id.__str__(), user_claims=another_claims, expires_time=expires_fresh)
            return JSONResponse({
                    "success": True,
                    "data": {
                        "access_token": new_access_token,
                        "refresh_token": new_refresh_token
                    }
                })
        except Exception as e:
            error = e.__class__.__name__
            if error == 'MissingTokenError':
                raise HTTPException(
                    status_code=status.HTTP_421_UNPROCESSABLE_ENTITY, detail={
                        'status': False,
                        'msg': 'Please provide refresh token'
                    })
            raise HTTPException(status_code=status.HTTP_421_UNPROCESSABLE_ENTITY,
                                detail={'status': False, 'msg': error})
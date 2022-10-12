from typing_extensions import Self
from fastapi import HTTPException, Depends, status
from fastapi_another_jwt_auth import AuthJWT

class RoleChecker:
    """
    RoleChecker

    Esta clase comprueba a partir de un diccionario si el rol almacenado en el 
    JWT Token del usuario en sesion tiene los permisos 
    para realizar sus respectivas acciones, en caso contrario
    se levanta una HTTPExecption, y se llama a esta 
    en las rutas como una dependencia.

    def __init__(self, allowed_roles: dict):

    - Esta funcion nos sirve para almacenar los roles en diccionario
    Es nuestro parametro

    def __call__(self, Authorize: AuthJWT = Depends()):
    - Mandamos a traer el JWT en sesion
    - Obtenemos el role de usuario en session
    - Si no esta el rol en nuestra lista levantamos una HTTPExcption
    """

    def __init__(self: Self, allowed_permissions: dict) -> None:
        self.allowed_permissions = allowed_permissions

    def __call__(self: Self, Authorize: AuthJWT = Depends()) -> None:
        Authorize.jwt_required()
        permissions = Authorize.get_raw_jwt()["permissions"]

        #print("Datos del token: ", permissions)
        #print("Lo que seteamos en la ruta: ", self.allowed_permissions)

        if self.allowed_permissions['module'] in permissions \
                and self.allowed_permissions['permission'] \
                in permissions[self.allowed_permissions['module']]:
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                headers={"WWW-Authenticate": "Bearer"},
                detail={"success": False,
                        "msg": "Tú no tienes acceso a este recurso."})

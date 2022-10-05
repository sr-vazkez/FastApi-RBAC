import inspect
import re

from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from app import models
from app.schemas import schemas_config
from app.database.main import engine
from app.routers import auth, role_actions, users, roles, module, actions, profile

#Se instancia FastAPI
app = FastAPI()

#Se habilitan cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    """
    Se crea esta funcion para habilitar la funcionalidad en Swagger
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Spuky - API",
        version="0.1.4",
        description="API Base for Projects",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
        }
    }
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
        "backgroundColor": "#000000",
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]
    
    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route, "endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint)) or
                re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
                re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {
                        "Bearer Auth": []
                    }
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

#Se genera documentacion personalizada
app.openapi = custom_openapi

@AuthJWT.load_config  # type: ignore
def get_config():
    """Se obtiene la configuracion para JWT Auth la cual debe de regresar un objeto de tipo AuthJWTConfig"""
    return schemas_config.Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    """
    Se crea esta funcion para manejar las excepciones de JWT Auth
    Retorna un objeto JSON con el error
    """
    return JSONResponse(
        status_code=421,  # type: ignore
        content={
            "success": False,
            "msg": exc.message # type: ignore
            }
    )

# Se genera la bd
models.Base.metadata.create_all(bind=engine)

# Se manean las rutas de cada modulo
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(module.router)
app.include_router(actions.router)
app.include_router(role_actions.router)

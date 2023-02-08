import logging

from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, Request
from fastapi_another_jwt_auth import AuthJWT
from fastapi_another_jwt_auth.exceptions import AuthJWTException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import models
from app.database.main import engine
from app.extras.custom_doc_openapi import custom_openapi
from app.extras.custom_json_format import CustomJsonFormatter
from app.routers import auth, role_actions, users, roles, module, actions, profile
from app.schemas import schemas_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()

formatter = CustomJsonFormatter(
    "%(@timestamp)s %(log.level)s %(log.logger)s %(message)s"
)


fh = RotatingFileHandler(
    "log_app/log.json",
    mode="a",
    maxBytes=50 * 1024 * 1024,
    backupCount=3,
    encoding="UTF-8",
    delay=0,
)

ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(fh)  # Exporting logs to a file

settings = schemas_config.SettingsDoc()

# Se instancia FastAPI
app = FastAPI(
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=settings.openapi_url,
)


#Se habilitan cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

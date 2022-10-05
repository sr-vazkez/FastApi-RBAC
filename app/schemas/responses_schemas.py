from app.schemas import schemas_config


responses = {
    400: {"model": schemas_config.Message},
    401: {"model": schemas_config.Message},
    403: {"model": schemas_config.MessagePermission},
}

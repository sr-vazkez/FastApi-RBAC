import inspect
import re
from app import main  # noqa
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi


def custom_openapi():
    """Se crea esta funcion para habilitar la funcionalidad en Swagger."""
    if main.app.openapi_schema:
        return main.app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI RBAC",
        version="0.1.61",
        description="API Base for all Projects",
        routes=main.app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
        }
    }
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
        "backgroundColor": "#000000",
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in main.app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route, "endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint))
                or re.search("fresh_jwt_required", inspect.getsource(endpoint))  # noqa
                or re.search("jwt_optional", inspect.getsource(endpoint))  # noqa
                or re.search(  # noqa
                    "jwt_refresh_token_required", inspect.getsource(endpoint)
                )
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {"Bearer Auth": []}
                ]

    main.app.openapi_schema = openapi_schema
    return main.app.openapi_schema

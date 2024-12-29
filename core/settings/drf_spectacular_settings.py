from .base_settings import PROJECT_NAME

# -------------------------------------
# DRF_SPECTACULAR CONFIGURATIONS
# -------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": f"{PROJECT_NAME}",
    "DESCRIPTION": f"{PROJECT_NAME} API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SCHEMA_PATH_PREFIX": r"/api/",
    # "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.3",
    # OTHER SETTINGS
}

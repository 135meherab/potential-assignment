from .base_settings import PROJECT_NAME, env

# -------------------------------------
# EMAIL: configurations
# -------------------------------------
if env.bool("USE_PRODUCTION_EMAIL", False):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL", default=f"{PROJECT_NAME} <{EMAIL_HOST_USER}>"
)

import json
import os
from datetime import timedelta
from pathlib import Path

import firebase_admin
from decouple import config
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APP_TEMPLATE_DIR = BASE_DIR.joinpath("templates")
APP_STATIC_DIR = BASE_DIR.joinpath("static")
APP_STATIC_ROOT = BASE_DIR.joinpath("staticfiles")
APP_MEDIA_ROOT = BASE_DIR.joinpath("media")

print(BASE_DIR)
# -------------------------------------
# SOLAPI: Configuration
# -------------------------------------
SOLAPI_API_KEY = os.getenv("SOLAPI_API_KEY")
SOLAPI_API_SECRET = os.getenv("SOLAPI_API_SECRET")

# -------------------------------------
# DJANGO: Configuration
# -------------------------------------
APP_DEBUG = os.getenv("DEBUG") == "True"
APP_SECRET_KEY = os.getenv("SECRET_KEY")
APP_ALLOWED_HOST = os.getenv("ALLOWED_HOSTS").split(",")
APP_CORS_HOSTS = os.getenv("CORS_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")

# -------------------------------------
# DATABASE: configurations
# -------------------------------------
DB_ENGINE = os.getenv("DB_ENGINE", default="django.db.backends.sqlite3")
DB_NAME = os.getenv("DB_NAME", default=BASE_DIR / "db.sqlite3")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# -------------------------------------
# REDIS: configurations
# -------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", default="localhost")

# -------------------------------------
# SYSTEM: configurations
# -------------------------------------
LOGOUT_ON_PASSWORD_CHANGE = os.getenv("LOGOUT_ON_PASSWORD_CHANGE") == "True"
REST_SESSION_LOGIN = os.getenv("REST_SESSION_LOGIN") == "True"
DEFAULT_OTP_SECRET = os.getenv(
    "DEFAULT_OTP_SECRET", default="1234567890"
)  # default OTP Secret Key
# OTP Verification True will send otp code to user while registration
OTP_ENABLED = os.getenv("OTP_ENABLED") == "True"
OTP_EXPIRY = os.getenv("OTP_EXPIRY", default="30")  # OTP Expiry Time

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = APP_SECRET_KEY

FERNET_SECRET_KEY = os.getenv(
    "FERNET_SECRET_KEY", default="bhcTDnLm8eii39PHQ0g34uyDfxiSBIq__YQtPmufkFg="
)  # Encryption Secret Key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = APP_DEBUG

ALLOWED_HOSTS = APP_ALLOWED_HOST

# Application definition


INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Library packages
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "fcm_django",  # Firebase Cloud Messaging For push notifications
    "debug_toolbar",  # django debug toolbar
    "dj_rest_auth",
    # created apps
    "authentications",
    "chat",
    "notice",
    "notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # debug toolbar
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APP_TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
# AUTHENTICATION:  auth user model
AUTH_USER_MODEL = "authentications.User"

# WSGI_APPLICATION = "core.wsgi.application" # WSGI Application
ASGI_APPLICATION = "core.asgi.application"  # To run websockets use ASGI Application

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": DB_ENGINE,
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

"""
=====REST_FRAMEWORK Configurations=====
PERMISSIONS: DjangoModelPermissionsOrAnonReadOnly
AUTHENTICATION: BasicAuthentication, SessionAuthentication, JWTAuthentication
SCHEMA_CLASS: AutoSchema drf_spectacular
FILTER_BACKEND: DjangoFilterBackend
DEFAULT_PAGINATION_CLASS: PageNumber
"""
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.BrowsableAPIRenderer",
        "utils.extensions.custom_renderer.CustomJSONRenderer",
    ),
    "DEFAULT_PAGINATION_CLASS": "utils.extensions.custom_pagination.CustomPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
AUTHENTICATION_BACKENDS = ["authentications.auth_backend.EmailAuthenticationBackend"]
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": APP_SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# -------------------------------------
# DRF_SPECTACULAR CONFIGURATIONS
# -------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "Potential Inc",
    "DESCRIPTION": "Potential Django Boilerplate API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SCHEMA_PATH_PREFIX": r"/api/",
    # "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.3",
    # OTHER SETTINGS
}
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = APP_STATIC_ROOT
STATICFILES_DIRS = [APP_STATIC_DIR]

# whitenoise
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
WHITENOISE_AUTOREFRESH = True

MEDIA_URL = "/media/"
MEDIA_ROOT = APP_MEDIA_ROOT

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------
# CHANNELS CONFIGURATION
# -------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, 6379)],
        },
    },
}

# -------------------------------------
# CACHE CONFIGURATION
# -------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# -------------------------------------
# EMAIL: configurations
# -------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL") == "True"
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL", default=f"Potential <{EMAIL_HOST_USER}>"
)

# -------------------------------------
# FIREBASE: Configurations
# -------------------------------------
cred = credentials.Certificate("google-services.json")
FIREBASE_MESSAGING_APP = firebase_admin.initialize_app(cred)
# FIREBASE_APP = initialize_app()
FCM_DJANGO_SETTINGS = {
    # an instance of firebase_admin.App to be used as default for all fcm-django requests
    # default: None (the default Firebase app)
    "DEFAULT_FIREBASE_APP": FIREBASE_MESSAGING_APP,
    # default: _('FCM Django')
    "APP_VERBOSE_NAME": "[Potential]",
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": False,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": False,
}

# -------------------------------------
# DJANGO DEBUG TOOLBAR: Configurations
# -------------------------------------
INTERNAL_IPS = [
    "127.0.0.1",
]

import os

from .base_settings import BASE_DIR

gettext = lambda s: s
LANGUAGES = (
    ("en", gettext("English")),
    ("ko", gettext("Korean")),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
USE_L10N = True
# LANGUAGE_CODE = 'en'  # Set default language

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

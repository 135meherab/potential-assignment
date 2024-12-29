from .base_settings import env

# -------------------------------------
# REDIS: envurations
# -------------------------------------
REDIS_HOST = env("REDIS_HOST", default="localhost")
REDIS_PORT = env("REDIS_PORT", default="6379")
REDIS_DB = env("REDIS_DB", default="0")
REDIS_PASSWORD = env("REDIS_PASSWORD", default="")

# -------------------------------------
# CHANNELS envURATION
# -------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "env": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# -------------------------------------
# CACHE envURATION
# -------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_PASSWORD}{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

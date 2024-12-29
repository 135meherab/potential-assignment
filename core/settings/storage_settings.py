from .base_settings import env

USE_S3 = env.bool("USE_S3", True)

if USE_S3:
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")  # AWS IAM user access key
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")  # AWS IAM user secret key
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")  # bucket name
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")  # region name
    AWS_S3_CUSTOM_DOMAIN = env(
        "CUSTOM_DOMAIN"
    )  # custom domain name from s3 or cloudfront
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }  # cache control settings
    AWS_QUERYSTRING_EXPIRE = int(
        env("AWS_QUERYSTRING_EXPIRE")
    )  # query string expire time
    AWS_LOCATION = f"{env('AWS_LOCATION')}"  # folder name in the bucket

    CLOUDFRONT_KEY_ID = env("CLOUDFRONT_KEY_ID")  # cloudfront key id
    AWS_CLOUDFRONT_KEY = env("AWS_CLOUDFRONT_KEY").replace(
        "\\n", "\n"
    )  # cloudfront private key

    # static files settings
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"  # static files url
    STORAGES = {
        "default": {
            "BACKEND": "core.storages.s3.PrivateMediaStorage",  # For media files
        },
        "staticfiles": {
            "BACKEND": "core.storages.s3.StaticFilesStorage",  # For static files
        },
    }

else:
    STATIC_URL = "static/"
    STATIC_ROOT = "static/"

    MEDIA_ROOT = "media/"
    MEDIA_URL = "media/"

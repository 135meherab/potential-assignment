from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticFilesStorage(S3Boto3Storage):
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    location = f"{settings.AWS_LOCATION}/static"
    default_acl = "private"
    # querystring_expire = settings.AWS_QUERYSTRING_EXPIRE
    #
    cloudfront_key_id = None
    cloudfront_key = None

    # def url(self, name, parameters=None, expire=None, http_method=None):
    #     # Override the url method to return unsigned URLs for static files
    #     url = super().url(name, parameters=parameters, expire=None, http_method=http_method)
    #
    #     # Remove any query parameters (which might be for signing)
    #     url = url.split('?')[0]
    #
    #     return url


class PublicMediaStorage(S3Boto3Storage):
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    location = f"{settings.AWS_LOCATION}/media"
    file_overwrite = False
    default_acl = "public-read"
    querystring_expire = settings.AWS_QUERYSTRING_EXPIRE


class PrivateMediaStorage(S3Boto3Storage):
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    cloudfront_key_id = settings.CLOUDFRONT_KEY_ID
    cloudfront_key = settings.AWS_CLOUDFRONT_KEY
    querystring_expire = settings.AWS_QUERYSTRING_EXPIRE
    location = f"{settings.AWS_LOCATION}/private"
    default_acl = "private"
    file_overwrite = False
    # custom_domain = False
    signature_version = "s3v4"
    addressing_style = "virtual"

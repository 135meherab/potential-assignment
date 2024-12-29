import datetime
import random
from typing import Literal

from dj_rest_auth.app_settings import api_settings
from django.conf import settings
from django.contrib.auth import login
from django.utils import timezone
from django.utils.translation import gettext as _
from pyotp import TOTP
from rest_framework import exceptions, response, status
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken

from authentications.models import User
from utils.helper import encode_token, encrypt
from utils.modules import EmailSender
from utils.modules.sms_sender import BulkSMSBDNet, SolApiClient


def get_origin(request):
    try:
        return request.headers["origin"]
    except Exception as e:
        raise exceptions.PermissionDenied(
            detail=_("Origin not found on request header")
        ) from e


def set_jwt_access_cookie(resp, access_token, domain):
    cookie_name = api_settings.JWT_AUTH_COOKIE
    access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
    cookie_secure = api_settings.JWT_AUTH_SECURE
    cookie_httponly = api_settings.JWT_AUTH_HTTPONLY
    cookie_samesite = api_settings.JWT_AUTH_SAMESITE
    cookie_domain = domain or api_settings.JWT_AUTH_COOKIE_DOMAIN

    if cookie_name:
        resp.set_cookie(
            cookie_name,
            access_token,
            expires=access_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            domain=cookie_domain,
        )


def set_jwt_refresh_cookie(resp, refresh_token, domain):
    refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
    refresh_cookie_name = api_settings.JWT_AUTH_REFRESH_COOKIE
    refresh_cookie_path = api_settings.JWT_AUTH_REFRESH_COOKIE_PATH
    cookie_secure = api_settings.JWT_AUTH_SECURE
    cookie_httponly = api_settings.JWT_AUTH_HTTPONLY
    cookie_samesite = api_settings.JWT_AUTH_SAMESITE
    cookie_domain = domain or api_settings.JWT_AUTH_COOKIE_DOMAIN

    if refresh_cookie_name:
        resp.set_cookie(
            refresh_cookie_name,
            refresh_token,
            expires=refresh_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            path=refresh_cookie_path,
            domain=cookie_domain,
        )


def set_jwt_cookies(domain: str | None, resp, access_token, refresh_token):
    # try:
    #     domain = origin.split("//")[1].split(":")[0]
    # except Exception as e:
    #     domain = None
    set_jwt_access_cookie(resp, access_token, domain)
    set_jwt_refresh_cookie(resp, refresh_token, domain)


def unset_jwt_cookies(resp, domain):
    cookie_name = api_settings.JWT_AUTH_COOKIE
    refresh_cookie_name = api_settings.JWT_AUTH_REFRESH_COOKIE
    refresh_cookie_path = api_settings.JWT_AUTH_REFRESH_COOKIE_PATH
    cookie_samesite = api_settings.JWT_AUTH_SAMESITE
    cookie_domain = domain or api_settings.JWT_AUTH_COOKIE_DOMAIN

    if cookie_name:
        resp.delete_cookie(cookie_name, samesite=cookie_samesite, domain=cookie_domain)
    if refresh_cookie_name:
        resp.delete_cookie(
            refresh_cookie_name,
            path=refresh_cookie_path,
            samesite=cookie_samesite,
            domain=cookie_domain,
        )


def direct_login(request, resp, user: User, token_data, social: bool = False):
    if settings.REST_AUTH.get("SESSION_LOGIN", False):
        login(request, user)

    # resp = response.Response()
    from urllib.parse import urlparse

    # print(request.headers.get("origin"))
    # print(request.META.get('HTTP_ORIGIN', ''))
    # origin = get_origin(request)
    # print(urlparse(origin).netloc if origin else None)

    set_jwt_cookies(
        # origin=get_origin(request),
        domain=None,
        resp=resp,
        access_token=token_data.get(
            settings.REST_AUTH.get("JWT_AUTH_COOKIE", "access"),
        ),
        refresh_token=token_data.get(
            settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE", "refresh"),
        ),
    )
    if not social:
        resp.data = {"data": token_data, "detail": _("Logged in successfully")}
        resp.status_code = status.HTTP_200_OK
    return resp


def generate_and_send_otp(
    user: User,
    otp_method: Literal["sms", "email"],
    generate_secret: bool = False,
    **kwargs,
):
    otp = TOTP(
        user.user_two_step_verification.secret_key,
        interval=settings.TOKEN_TIMEOUT_SECONDS,
    )

    otp_code = otp.now()
    if otp_method == "sms":
        # sms send for otp code
        send_verification_sms(user.user_information.phone_number, otp_code)
    elif otp_method == "email":
        # email send for otp code
        send_otp_email(user, otp_code)

    return response.Response(
        {
            "data": {
                "secret": generate_token(user, **kwargs) if generate_secret else None,
                "otp_method": otp_method,
                "detail": _(
                    f"OTP is active for {settings.TOKEN_TIMEOUT_SECONDS} seconds"
                ),
            },
            "message": _("OTP is Sent"),
        },
        status=status.HTTP_200_OK,
    )


def generate_link(user: User, origin: str, route: str, **kwargs) -> str:
    return f"{origin}/auth/{route}/{generate_token(user, **kwargs)}/"


def generate_token(user: User, **kwargs):
    payload = {
        "user": str(user.id),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(seconds=settings.TOKEN_TIMEOUT_SECONDS),
        **kwargs,
    }
    token = encrypt(encode_token(payload=payload)).decode()
    return token


def generate_otp(user: User):
    otp = f"{user.id}{random.randint(10000, 99999)}"
    return otp


def send_otp_email(user, otp):
    body = f"One time verification code is {otp}"
    email = EmailSender(send_to=[user.email], subject="OTP Verification", body=body)
    email.send_email()


def send_verification_email(user, link):
    body = f"Your Verification is {link}"
    email = EmailSender(send_to=[user.email], subject="OTP Verification", body=body)
    email.send_email()


def send_verification_sms(phone_number, code):
    body = _(f"One time verification code is {code}")
    solapi = SolApiClient()
    solapi.send_one(phone_number, body)
    # solapi.get_balance()
    # bulk_sms_bd = BulkSMSBDNet()
    # bulk_sms_bd.send_sms(phone_number, body)
    print(body)


def get_token(user):
    token = RefreshToken.for_user(user)
    token["email"] = user.email
    token["is_staff"] = user.is_staff
    token["is_active"] = user.is_active
    token["is_superuser"] = user.is_superuser
    return token


def extract_token(refresh_token: RefreshToken) -> dict:
    return {
        settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE", "refresh"): str(
            refresh_token
        ),
        settings.REST_AUTH.get("JWT_AUTH_COOKIE", "access"): str(
            refresh_token.access_token
        ),
    }

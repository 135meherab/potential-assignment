import contextlib

from cryptography.fernet import InvalidToken as FernetInvalidToken
from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.urls import resolve
from django.utils.translation import gettext as _
from jwt import ExpiredSignatureError
from pyotp import TOTP
from rest_framework import exceptions, generics, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentications.models import User
from utils.helper import decode_token, decrypt


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        request = self.context.get("request")
        if resolve(request.path_info).url_name.split("-")[0] != self.user.role:
            raise exceptions.AuthenticationFailed(
                self.default_error_messages["no_active_account"]
            )

        if settings.SIMPLE_JWT.get("UPDATE_LAST_LOGIN"):
            update_last_login(None, self.user)

        return data, self.user

    def get_token(self, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["is_active"] = user.is_active
        token["is_superuser"] = user.is_superuser
        return token


class OTPLoginSerializer(serializers.Serializer):
    """
    Serializer to log in with OTP
    """

    secret = serializers.CharField(write_only=True)
    otp = serializers.IntegerField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payload = None
        self.user = None

    def validate_secret(self, value):
        try:
            self.payload = decode_token(decrypt(value))
        except FernetInvalidToken as e:
            raise serializers.ValidationError(_("Invalid OTP Secret")) from e
        except ExpiredSignatureError as e:
            raise serializers.ValidationError(_("OTP Secret Expired")) from e
        return value

    def validate_otp(self, value):
        with contextlib.suppress(AttributeError):
            self.user: User = generics.get_object_or_404(
                User, id=self.payload.get("user")
            )

            if self.user.user_two_step_verification.otp_method == "authenticator_app":
                otp = TOTP(self.user.user_two_step_verification.secret_key)
                if not otp.verify(value):
                    raise serializers.ValidationError(_("Invalid OTP"))
            else:
                otp = TOTP(
                    self.user.user_two_step_verification.secret_key,
                    interval=settings.TOKEN_TIMEOUT_SECONDS,
                )
                if not otp.verify(value):
                    raise serializers.ValidationError(_("Invalid OTP"))
            return value


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(write_only=True)
    otp_method = serializers.ChoiceField(
        choices=["authenticator_app", "email", "sms"],
        write_only=True,
        default="authenticator_app",
    )

    def validate_otp(self, value):
        request = self.context.get("request")
        if (
            self.initial_data.get("otp_method", "authenticator_app")
            == "authenticator_app"
        ):
            otp = TOTP(request.user.user_two_step_verification.secret_key)
            if not otp.verify(value):
                raise serializers.ValidationError(_("Invalid OTP"))
        else:
            otp = TOTP(
                request.user.user_two_step_verification.secret_key,
                interval=settings.TOKEN_TIMEOUT_SECONDS,
            )
            if not otp.verify(value):
                raise serializers.ValidationError(_("Invalid OTP"))
        return value


class FCMDeleteSerializer(serializers.Serializer):
    device_id = serializers.CharField(write_only=True)

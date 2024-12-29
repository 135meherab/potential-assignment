import jwt
from cryptography import fernet
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import (
    decorators,
    exceptions,
    permissions,
    response,
    status,
    viewsets,
)
from rest_framework_simplejwt.exceptions import InvalidToken

from authentications import serializers
from authentications.models import User
from authentications.views.common_functions import (
    direct_login,
    extract_token,
    generate_link,
    get_origin,
    get_token,
    send_verification_email,
)
from utils.extensions.permissions import IsAuthenticatedAndEmailNotVerified
from utils.helper import decode_token, decrypt


class RegistrationView(viewsets.GenericViewSet):
    """
    New User Create View
    """

    serializer_class = serializers.RegistrationSerializer
    queryset = User.objects.all()
    permission_classes = ()

    # authentication_classes = ()

    # http_method_names = ["post"]

    def _login(self, user, message: str):
        token = extract_token(get_token(user))
        resp = direct_login(
            request=self.request, resp=response.Response(), user=user, token_data=token
        )

        resp.data["data"]["message"] = message
        return resp

    def _verification_email(self, user):
        context = {
            "url": generate_link(user, get_origin(self.request), "verify-email"),
        }

        is_email_verification_required = settings.REQUIRED_EMAIL_VERIFICATION

        if is_email_verification_required:
            send_verification_email(user, context)
        if self.action == "create":
            resp = self._login(
                user,
                (
                    _("Verification Email Sent")
                    if is_email_verification_required
                    else _("Account Created Successfully")
                ),
            )
            return resp
        return response.Response(
            data={"data": _("Verification Email Sent")}, status=status.HTTP_200_OK
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return self._verification_email(user=user)

    @decorators.action(
        detail=False,
        url_path="resend-verification-email",
        methods=["get"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def resend_verification_email(self, *args, **kwargs):
        """
        resend_mail method for resending verification email
        """

        user = self.request.user
        if user.is_verified:
            raise exceptions.PermissionDenied(detail=_("Email already verified"))
        if user.email:
            return self._verification_email(user=user)

        raise exceptions.PermissionDenied(
            detail=_("No Email found!!!"),
        )

    @decorators.action(
        detail=False,
        url_path="verify-email/(?P<token>[^/.]+)",
        methods=["get"],
        # permission_classes=(IsAuthenticatedAndEmailNotVerified,),
    )
    def verify_email(self, *args, **kwargs):
        try:
            data = decode_token(token=decrypt(kwargs.get("token")))
            try:
                user = User.objects.get(id=data["user"])
                if user.is_verified:
                    return response.Response(
                        {
                            "data": _("Email Already Verified"),
                        }
                    )
                user.is_verified = True
                user.save()
            except (User.DoesNotExist, ValidationError) as e:
                raise exceptions.NotFound(detail=e) from e
        except fernet.InvalidToken as e:
            raise InvalidToken(detail=str(e)) from e
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.DecodeError,
        ) as e:
            raise exceptions.ValidationError(detail={"detail": e}) from e
        return response.Response({"data": _("Email Verification Successful")})


class AdminUserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all().select_related(
        "user_information",
        "user_information__language",
        "user_information__country",
        "user_information__province",
        "user_information__city",
    )
    serializer_class = serializers.AdminUserSerializer
    filterset_fields = ["role"]
    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "head",
        "options",
        "trace",
    ]

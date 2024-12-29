from django.utils.translation import gettext as _
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import exceptions, generics
from rest_framework.response import Response

from authentications import serializers
from authentications.views.common_functions import (
    generate_and_send_otp,
    generate_link,
    generate_token,
    get_origin,
    send_verification_email,
)
from utils import helper
from utils.extensions import validate_query_params


# ============***********============
# Password reset views
# ============***********============
class ResetPasswordView(generics.GenericAPIView):
    """
    View for getting email or sms for password reset
    post: email: ""
    """

    serializer_class = serializers.ResetPasswordSerializer
    authentication_classes = []
    permission_classes = []

    # throttle_classes = (AnonUserRateThrottle,)

    @staticmethod
    def email_sender_helper(user, origin, verification_method):
        url = generate_link(
            user, origin, "reset-password", verification_method=verification_method
        )
        send_verification_email(user, url)

        return Response({"data": {"detail": _("Verification Email Sent")}})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "verification_method",
                type={"type": "string"},
                enum=["email", "sms"],
                default="email",
                style="form",
                explode=False,
                required=True,
            ),
        ]
    )
    @validate_query_params("verification_method", ["email", "sms"])
    def post(self, request, *args, **kwargs):
        verification_method = self.request.query_params.get(
            "verification_method", "email"
        )

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if not user.email:
            raise exceptions.PermissionDenied(detail="No Email found!!!")

        if verification_method == "sms":
            return generate_and_send_otp(
                user, "sms", True, verification_method=verification_method
            )
        else:
            return self.email_sender_helper(
                user, get_origin(self.request), verification_method
            )


class ResetPasswordCheckView(generics.GenericAPIView):
    """
    View for checking if the url is expired or not
    post: token: ""
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.ResetPasswordCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "data": {
                    "detail": "Accepted",
                    "secret": generate_token(
                        serializer.user,
                        reset_password=True,
                        verification_method=serializer.verification_method,
                    ),
                }
            }
        )


class ResetPasswordConfirmView(generics.GenericAPIView):
    """
    View for resetting password after checking the token
    post: secret: "", password: ""
    """

    serializer_class = serializers.ResetPasswordConfirmSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        return self._change_password(serializer)

    @staticmethod
    def _change_password(serializer):
        user = serializer.user
        user.set_password(serializer.validated_data.get("password"))
        user.save(update_fields=["password"])
        return Response({"detail": _("Password Changed Successfully")})

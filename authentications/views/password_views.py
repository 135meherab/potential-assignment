from dj_rest_auth.jwt_auth import unset_jwt_cookies
from django.conf import settings
from django.contrib.auth import logout
from django.utils.translation import gettext as _
from rest_framework import generics, response, status, views

from authentications import serializers
from utils.extensions.permissions import IsAuthenticatedAndEmailVerified


class PasswordValidateView(views.APIView):
    """
    View for validating password
    """

    permission_classes = (IsAuthenticatedAndEmailVerified,)
    serializer_class = serializers.PasswordValidateSerializer

    def post(self, request, *args, **kwargs):
        current_user = self.request.user
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        if current_user.check_password(
            serializer.validated_data.get("password"),
        ):
            return response.Response(
                {"message": _("Password Accepted")}, status=status.HTTP_200_OK
            )
        return response.Response(
            {"message": _("Wrong Password")},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    permission_classes = (IsAuthenticatedAndEmailVerified,)
    serializer_class = serializers.ChangePasswordSerializer

    @staticmethod
    def _logout_on_password_change(request, message):
        resp = response.Response(
            {"detail": message},
            status=status.HTTP_200_OK,
        )
        if settings.REST_SESSION_LOGIN:
            logout(request)
        unset_jwt_cookies(resp)
        return resp

    def _change_password(self, request, user, password):
        user.set_password(password)
        user.save()
        message = _("Password updated successfully")
        if settings.REST_AUTH.get("LOGOUT_ON_PASSWORD_CHANGE"):
            self._logout_on_password_change(request=request, message=message)

        return response.Response(
            {"detail": message},
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password")
        return self._change_password(
            request=request,
            user=user,
            password=password,
        )

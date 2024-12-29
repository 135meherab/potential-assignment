from django.conf import settings
from rest_framework import permissions, response, viewsets

from payment.serializers import MakePaymentSerializers
from utils.modules.payment import AuthorizeNet


class MakePaymentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MakePaymentSerializers

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


class GetSavedCardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def list(request):
        authorize_net = AuthorizeNet(
            api_login_id=settings.AUTHORIZE_NET_API_LOGIN_ID,
            transaction_key=settings.AUTHORIZE_NET_TRANSACTION_KEY,
        )
        response_data = authorize_net.get_customer_profile(
            request.user.user_information.authorizenet_customer_profile_id
        )
        return response.Response(response_data)

    def retrieve(self, request, pk=None):
        authorize_net = AuthorizeNet(
            api_login_id=settings.AUTHORIZE_NET_API_LOGIN_ID,
            transaction_key=settings.AUTHORIZE_NET_TRANSACTION_KEY,
        )
        response_data = authorize_net.get_customer_payment_profile(
            request.user.user_information.authorizenet_customer_profile_id, pk
        )
        return response.Response(response_data)

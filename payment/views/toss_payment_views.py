from django.utils.translation import gettext as _
from rest_framework import response, viewsets
from rest_framework.permissions import IsAuthenticated

from payment.models import Order
from payment.serializers import (
    CancelPaymentSerializer,
    OrderSerializer,
    PaymentSerializer,
)
from utils.extensions.permissions import IsAdmin, IsAdminOrTeacherOwner, IsStudent


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user", "user__user_information", "course")
    serializer_class = OrderSerializer
    http_method_names = ["get", "post"]

    def get_permissions(self):
        # Only student can create an order
        if self.action == "create":
            permission_classes = [IsAuthenticated, IsStudent]
        else:
            permission_classes = [IsAuthenticated, IsAdminOrTeacherOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.role == "student":
            return self.queryset.filter(user=self.request.user)
        elif self.request.user.role == "teacher":
            return self.queryset.filter(course__teacher=self.request.user)
        return self.queryset.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = PaymentSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"message": _("Payment successful.")})


class CancelPaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = CancelPaymentSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"message": _("Payment cancelled.")})

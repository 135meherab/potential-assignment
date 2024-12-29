from rest_framework import viewsets

from orders.models import Order
from orders.serializers import OrderSerializer
from utils.extensions.permissions import IsVendor


class VendorOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsVendor]

    def get_queryset(self):
        return Order.objects.filter(order_items__product__vendor=self.request.user)

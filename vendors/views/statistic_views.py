from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from products.models import ProductModel


class VendorAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor = request.user
        total_products = ProductModel.objects.filter(vendor=vendor).count()
        total_orders = Order.objects.filter(order_items__product__vendor=vendor).count()
        total_revenue = sum(
            order.total_cost
            for order in Order.objects.filter(order_items__product__vendor=vendor)
        )

        analytics_data = {
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
        }

        return Response(analytics_data)

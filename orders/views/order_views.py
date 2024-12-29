from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Cart, CartItems, Order, OrderItems
from orders.serializers import OrderSerializer


class CheckoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        cart = Cart.objects.get(user=request.user)
        total_cost = sum(
            item.product.price * item.quantity for item in cart.cart_items.all()
        )

        shipping_name = request.data.get("shipping_name")
        shipping_address = request.data.get("shipping_address")
        shipping_phone = request.data.get("shipping_phone")

        order = Order.objects.create(
            user=request.user,
            shipping_name=shipping_name,
            shipping_address=shipping_address,
            shipping_phone=shipping_phone,
            total_cost=total_cost,
        )

        for cart_item in cart.cart_items.all():
            OrderItems.objects.create(
                order=order, product=cart_item.product, quantity=cart_item.quantity
            )

        cart.cart_items.all().delete()
        cart.delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

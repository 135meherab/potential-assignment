from OpenSSL.rand import status
from rest_framework.response import Response
from rest_framework import viewsets
from orders.models import CartItems, Cart
from orders.serializers import CartItemSerializer, CartSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
class CartViewSets(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        total_cost = sum(item.product.price * item.quantity for item in cart.cart_items.all())
        serializer = CartSerializer(cart)
        return Response({
                "cart": serializer.data,
                "total_cost": total_cost
        })

    def add_item(self,request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update_item(self, request, pk=None):
        try:
            cart_item = CartItems.objects.get(pk=pk, cart__user=request.user)
            quantity = request.data.get('quantity')
            if quantity is not None:
                cart_item.quantity = quantity
                cart_item.save()
            return Response(CartItemSerializer(cart_item).data)
        except CartItems.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def remove_item(self, request, pk=None):
        try:
            cart_item = CartItems.objects.get(pk=pk, cart__user=request.user)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItems.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

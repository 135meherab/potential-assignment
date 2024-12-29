from rest_framework import serializers
from orders.models import Cart, CartItems


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ["id", "product", "quantity"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]
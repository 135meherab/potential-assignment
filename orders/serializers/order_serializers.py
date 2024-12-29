from rest_framework import serializers

from orders.models import Order, OrderItems


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ["id", "product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "shipping_name",
            "shipping_address",
            "shipping_phone",
            "total_cost",
            "created_at",
            "items",
        ]

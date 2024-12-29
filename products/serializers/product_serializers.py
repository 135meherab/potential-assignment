from rest_framework import serializers

from products.models import ProductModel


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        exclude = ["vendor"]

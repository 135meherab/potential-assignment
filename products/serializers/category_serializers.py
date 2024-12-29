from rest_framework import  serializers
from products.models import CategoryModel, SubCategoryModel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryModel
        fields = "__all__"

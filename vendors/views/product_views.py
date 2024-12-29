from rest_framework import viewsets

from products.models import ProductModel
from products.serializers import ProductSerializer
from utils.extensions.permissions import IsVendor


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsVendor]

    def get_queryset(self):
        return ProductModel.objects.filter(vendor=self.request.user)

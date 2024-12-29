from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from products.serializers import ProductSerializer
from products.models import ProductModel


class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        if self.request.user.role == "vendor":
            serializer.save(vendor=self.request.user)
        else:
            raise PermissionDenied("Only vendors can create products.")
from products.serializers import CategorySerializer, SubCategorySerializer
from products.models import CategoryModel, SubCategoryModel
from rest_framework import viewsets
from utils.extensions.permissions import IsAdminOrReadOnly

class CategoryViewSets(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategoryModel.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return self.queryset
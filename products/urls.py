from django.urls import path
from rest_framework.routers import DefaultRouter

from products.views import CategoryViewSets, ProductViewSet, SubCategoryViewSet

router = DefaultRouter()

router.register("category", CategoryViewSets, basename="category")
router.register("sub-category", SubCategoryViewSet, basename="subcategory")
router.register("", ProductViewSet, basename="product")
urlpatterns = [] + router.urls

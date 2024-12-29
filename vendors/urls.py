from django.urls import path

from .views import ProductViewSet, VendorAnalyticsView, VendorOrderViewSet

urlpatterns = [
    path(
        "products/",
        ProductViewSet.as_view({"get": "list", "post": "create"}),
        name="product-list",
    ),
    path(
        "products/<int:pk>/",
        ProductViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="product-detail",
    ),
    path("vendor/analytics/", VendorAnalyticsView.as_view(), name="vendor_analytics"),
    path(
        "vendor/orders/",
        VendorOrderViewSet.as_view({"get": "list"}),
        name="vendor_orders",
    ),
    path(
        "vendor/orders/<int:pk>/",
        VendorOrderViewSet.as_view({"get": "retrieve"}),
        name="vendor_order_detail",
    ),
]

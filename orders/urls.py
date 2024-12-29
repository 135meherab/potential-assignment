from django.urls import path

from orders.models import CartItems
from orders.views import CartViewSets

urlpatterns = [
    path("cart/", CartViewSets.as_view({"get": "get_cart", "post": "add_item"}), name="cart"),
    path("cart/item/<int:pk>/", CartViewSets.as_view({"get": "update_item", "delete": "remove_item"}), name="cart-item")
]
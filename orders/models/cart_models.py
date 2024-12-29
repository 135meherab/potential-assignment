from authentications.models import *
from products.models import ProductModel


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, related_name="cart_product"
    )
    quantity = models.PositiveIntegerField(default=1)

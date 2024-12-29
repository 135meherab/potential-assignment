from authentications.models import User
from core.models import *
from products.models import ProductModel


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_user")
    shipping_name = models.CharField(max_length=255)
    shipping_address = models.TextField()
    shipping_phone = models.CharField(max_length=15)
    total_cost = models.IntegerField()

    def __str__(self):
        return f"Order {self.id}"


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

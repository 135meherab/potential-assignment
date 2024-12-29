import uuid

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class Order(BaseModel):
    STATUS = [
        ("PENDING", _("Pending")),
        ("PAYMENT_COMPLETE", _("Payment Complete")),
        ("PAYMENT_FAILED", _("Payment Failed")),
        ("CANCELLED", _("Cancelled")),
    ]
    order_id = models.CharField(max_length=255, unique=True, editable=False)
    user = models.ForeignKey(
        "authentications.User", on_delete=models.CASCADE, related_name="orders"
    )
    # Relationship with item. It can be a course, product, or any other item
    product = models.ForeignKey(
        "product.Products", on_delete=models.CASCADE, related_name="orders"
    )
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default="PENDING")
    payment_key = models.CharField(max_length=255, blank=True, null=True)
    payment_type = models.CharField(max_length=20, blank=True, null=True)
    payment_response = models.JSONField(null=True, blank=True)

    def clean(self):
        super().clean()
        # Check if there's any existing completed order for this user and product
        existing_complete_order = Order.objects.filter(
            user=self.user, product=self.product, status="PAYMENT_COMPLETE"
        ).exists()

        if existing_complete_order:
            raise ValidationError(
                {
                    "product": _("You have already purchased this product."),
                    "user": _("User has already purchased this product."),
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation before saving

        if not self.order_id:
            with transaction.atomic():
                # First save to get the pk
                self.order_id = f"TEMP-{uuid.uuid4()}"
                super().save(*args, **kwargs)
                # Now generate the order_id
                # "ORD{YEAR}{MONTH}{DAY}{MIN}{SEC}{MILISEC-TWO-DIGITS}{000000PK}"
                self.order_id = (
                    f"O{self.created_at.strftime('%Y%m%d%H%M%S%f')[:-3]}{self.pk}"
                )
                # self.order_id = (
                #     f"O{self.created_at.strftime('%Y%m%d%H%M%S%f')[:-3]}{self.pk:06d}"
                # )
                # Save again to store the generated order_id
                super().save(update_fields=["order_id"])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    class Meta:
        ordering = ["-created_at"]
        # Add unique constraint on user and product only if the payment is complete
        # Meaning if status is PAYMENT_COMPLETE, then the combination of user and product should be unique
        # Then the user and product can't have multiple orders with any of the statuses
        # This is to prevent duplicate orders for the same user and product
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                condition=models.Q(status="PAYMENT_COMPLETE"),
                name="unique_order",
            )
        ]

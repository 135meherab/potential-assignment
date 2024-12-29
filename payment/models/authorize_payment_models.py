from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class Payment(BaseModel):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        SUCCESS = "SUCCESS", _("Success")
        FAILED = "FAILED", _("Failed")

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", _("Cash")
        CARD = "CARD", _("Card")
        CHEQUE = "CHEQUE", _("Cheque")
        ONLINE = "ONLINE", _("Online")

    amount = models.FloatField()
    status = models.CharField(
        max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    method = models.CharField(
        max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return f"Payment of {self.amount} by {self.method}"

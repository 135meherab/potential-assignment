import pyotp
from course.models import Enrollment
from django.db.models.signals import post_save
from django.dispatch import receiver

from payment.models import Order


@receiver(post_save, sender=Order)
def create_enrollment(sender, instance, created, **kwargs):
    if instance.status == "PAYMENT_COMPLETE":
        Enrollment.objects.create(user=instance.user, course=instance.course)
    if instance.status == "CANCELLED":
        Enrollment.objects.filter(user=instance.user, course=instance.course).delete()

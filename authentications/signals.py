import pyotp
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentications.models import User, UserInformation, UserTwoStepVerification


@receiver(post_save, sender=User)
def create_user_instance(sender, instance, created, **kwargs):
    if created:
        # user two-step verification and user information instance creation
        UserTwoStepVerification.objects.create(
            user=instance, secret_key=pyotp.random_base32()
        )
        UserInformation.objects.create(
            user=instance,
        )

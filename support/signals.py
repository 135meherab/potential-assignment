from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message
from firebase_admin.messaging import Notification as FCM_Notification

from authentications.models import User
from support.models import InquiryAnswer, Notice, Notification


@receiver(post_save, sender=Notification)
def create_notification_instance(sender, instance, created, **kwargs):
    if created:
        # You can still use .filter() or any methods that return QuerySet (from the chain)
        devices = FCMDevice.objects.filter(user=instance.user)
        # send_message parameters include: message, dry_run, app
        devices.send_message(
            Message(
                notification=FCM_Notification(title=instance.title, body=instance.body),
                # topic="New",
            )
        )


@receiver(post_save, sender=Notice)
def create_notice_instance(sender, instance, created, **kwargs):
    if created:
        # You can still use .filter() or any methods that return QuerySet (from the chain)
        devices = FCMDevice.objects.all()
        # send_message parameters include: message, dry_run, app
        devices.send_message(
            Message(
                notification=FCM_Notification(
                    title=instance.title, body="You have a new notice"
                ),
                # topic="New",
            )
        )


@receiver(post_save, sender=InquiryAnswer)
def create_inquery_answer_instance(sender, instance, created, **kwargs):
    if created:
        # You can still use .filter() or any methods that return QuerySet (from the chain)
        devices = FCMDevice.objects.filter(user=instance.inquiry.user)
        instance.inquiry.is_answered = True
        instance.inquiry.save(update_fields=["is_answered"])
        # send_message parameters include: message, dry_run, app
        devices.send_message(
            Message(
                notification=FCM_Notification(
                    title="You have got a solution",
                    body="Your inquiry has just been answered. Check Now.",
                ),
                # topic="New",
            )
        )

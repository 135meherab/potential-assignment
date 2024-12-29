from rest_framework import serializers

from support.models import Notification


class NotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "body", "link", "created_at", "is_read")

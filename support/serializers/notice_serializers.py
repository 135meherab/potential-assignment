from rest_framework import serializers

from support.models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ("id", "title", "body", "image", "created_at")

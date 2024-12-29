from rest_framework import serializers

from site_settings.models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"
        read_only_fields = ["slug"]

from rest_framework import serializers

from site_settings.models import SiteInformation


class SiteInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteInformation
        fields = "__all__"

    def create(self, validated_data):
        # Only one Item is allowed, so create or update
        instance, created = SiteInformation.objects.update_or_create(
            defaults=validated_data,
        )
        return instance

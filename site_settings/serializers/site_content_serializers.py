from rest_framework import serializers

# from authentications.serializers import UserSerializer
from site_settings.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Banner
        fields = (
            "id",
            "short_text",
            "long_text",
            "background_color",
            "image",
            "link",
            "is_published",
        )

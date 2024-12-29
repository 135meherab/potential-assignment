from rest_framework import serializers


class SocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()

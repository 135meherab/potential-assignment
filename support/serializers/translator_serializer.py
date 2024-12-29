from rest_framework import serializers


class TranslatorSerializer(serializers.Serializer):
    text = serializers.CharField()
    target_lang = serializers.ChoiceField(
        choices=[("EN-US", "English"), ("KO", "Korean")], default="EN-US"
    )

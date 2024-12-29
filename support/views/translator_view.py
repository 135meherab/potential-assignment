import deepl
from django.conf import settings
from rest_framework import response, views

from support.serializers import TranslatorSerializer


class TranslatorView(views.APIView):
    permission_classes = ()
    serializer_class = TranslatorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data.get("text")
        target_lang = serializer.validated_data.get("target_lang")

        translator = deepl.Translator(settings.DEEPL_TRANSLATOR_API_KEY)
        translation = translator.translate_text(text, target_lang=target_lang)
        return response.Response({"data": translation.text})

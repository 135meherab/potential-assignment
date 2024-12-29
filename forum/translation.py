from modeltranslation.translator import TranslationOptions, register, translator

from forum.models import Tag


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("tag_name",)
    required_languages = ("en", "ko")


# translator.register(Interest, InterestTranslationOptions)

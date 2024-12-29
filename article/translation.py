from modeltranslation.translator import TranslationOptions, register, translator

from article.models import ArticleCategory


@register(ArticleCategory)
class ArticleCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)
    required_languages = ("en", "ko")


# translator.register(Interest, InterestTranslationOptions)

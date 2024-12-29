from modeltranslation.translator import TranslationOptions, register, translator

from options.models import City, Country, Language, Province


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ("country_long",)
    required_languages = ("en", "ko")


@register(Province)
class ProvinceTranslationOptions(TranslationOptions):
    fields = ("province_name",)
    required_languages = ("en", "ko")


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ("city_name",)
    required_languages = ("en", "ko")


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ("language_name",)
    required_languages = ("en", "ko")


# translator.register(Interest, InterestTranslationOptions)

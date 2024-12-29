from rest_framework import serializers

from options.models import City, Country, Language, Province


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "country_short", "country_long")


class CountryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "country_short", "country_long_en", "country_long_ko")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "city_name")


class CityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "province", "city_name_en", "city_name_ko")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["province"] = {
            "id": instance.province.id,
            "province_name": instance.province.province_name,
        }
        return response


class ProvinceSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = ("id", "province_name", "cities")


class OnlyProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = ("id", "province_name")


class ProvinceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ("id", "province_name_en", "province_name_ko")


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("id", "language_name")


class LanguageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("id", "language_name_en", "language_name_ko")

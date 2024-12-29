from rest_framework import permissions, response, views, viewsets

from options.models import City, Country, Language, Province
from options.serializers import (
    CityCreateSerializer,
    CountrySerializer,
    LanguageCreateSerializer,
    LanguageSerializer,
    ProvinceSerializer,
)
from utils.extensions.permissions import IsAdminOrReadOnly


class OptionsListView(views.APIView):
    """
    API endpoint to retrieve a list of interests, optionally filtered by language.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        country_queryset = Country.objects.all()
        countries = CountrySerializer(country_queryset, many=True)

        province_queryset = Province.objects.all().prefetch_related("cities")
        provinces = ProvinceSerializer(province_queryset, many=True)

        language_queryset = Language.objects.all()
        languages = LanguageSerializer(language_queryset, many=True)

        return response.Response(
            {
                "countries": countries.data,
                "provinces": provinces.data,
                "languages": languages.data,
            }
        )


class LanguageViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrReadOnly,
    )
    queryset = Language.objects.all()
    serializer_class = LanguageCreateSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrReadOnly,
    )


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.prefetch_related("cities").all()
    serializer_class = ProvinceSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrReadOnly,
    )


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("province").all()
    serializer_class = CityCreateSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrReadOnly,
    )

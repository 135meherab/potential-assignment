from rest_framework.routers import DefaultRouter

from options.views import CityViewSet, CountryViewSet, LanguageViewSet, ProvinceViewSet

router = DefaultRouter()
router.register(r"languages", LanguageViewSet, basename="languages")
router.register(r"provinces", ProvinceViewSet, basename="provinces")
router.register(r"cities", CityViewSet, basename="cities")
router.register(r"countries", CountryViewSet, basename="countries")

urlpatterns = []
urlpatterns += router.urls

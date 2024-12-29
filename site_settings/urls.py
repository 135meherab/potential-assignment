from django.urls import path
from rest_framework.routers import DefaultRouter

from site_settings.views import (
    BannerViewSet,
    DashboardViewSet,
    PageViewSet,
    SiteInformationViewSet,
)

# fcm push notifications urls
router = DefaultRouter()
router.register("pages", PageViewSet, basename="pages")
router.register("banner", BannerViewSet, basename="banner")
router.register("site-information", SiteInformationViewSet, basename="site-information")
router.register("dashboard", DashboardViewSet, basename="dashboard")
urlpatterns = []
urlpatterns += router.urls

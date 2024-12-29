from django.urls import path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet  # fcm urls
from rest_framework.routers import DefaultRouter

from support.views import (
    InquiryAnswerView,
    InquiryViewSet,
    NoticeViewSet,
    NotificationView,
    TranslatorView,
)

# fcm push notifications urls
router = DefaultRouter()
router.register(r"devices", FCMDeviceAuthorizedViewSet, basename="fcm")
router.register(r"inquiry", InquiryViewSet, basename="inquiry")
router.register(r"notice", NoticeViewSet, basename="notice")

urlpatterns = [
    path(
        "inquiry/<int:id>/answer/",
        InquiryAnswerView.as_view(),
        name="inquiry-details",
    ),
    path("notifications/", NotificationView.as_view(), name="user-notifications"),
    path("translate/", TranslatorView.as_view(), name="translator"),
]
urlpatterns += router.urls

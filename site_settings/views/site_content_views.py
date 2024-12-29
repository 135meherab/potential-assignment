from rest_framework import response, viewsets

from site_settings.models import Banner
from site_settings.serializers import BannerSerializer
from utils.extensions.permissions import IsAdminOrReadOnly


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.select_related("user", "user__user_information").all()
    serializer_class = BannerSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == "admin":
            return self.queryset
        return self.queryset.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

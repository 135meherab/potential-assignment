from rest_framework import response, viewsets

from site_settings.models import Page
from site_settings.serializers import PageSerializer
from utils.extensions.permissions import IsAdminOrReadOnly


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]

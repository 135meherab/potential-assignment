from django.db.utils import IntegrityError
from django.utils.translation import gettext as _
from rest_framework import exceptions, generics, permissions, response, viewsets

from support.models import Inquiry, InquiryAnswer
from support.serializers import InquiryAnswerSerializer, InquirySerializer
from utils.extensions.permissions import IsAdmin, IsAdminOrReadOnly


class InquiryViewSet(viewsets.ModelViewSet):
    serializer_class = InquirySerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"
    http_method_names = ["get", "post"]
    queryset = (
        Inquiry.objects.select_related("user__user_information")
        .prefetch_related("inquiry_answers")
        .all()
    )

    def get_queryset(self):
        if self.request.user.role == "admin":
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class InquiryAnswerView(generics.ListCreateAPIView):
    serializer_class = InquiryAnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = InquiryAnswer.objects.all()

    def check_permissions(self, request):
        user = request.user
        if not user.is_authenticated:
            raise exceptions.NotAuthenticated
        if user.role == "admin":
            return True
        inquiry_id = self.kwargs.get("id")
        inquiry = Inquiry.objects.filter(id=inquiry_id).first()
        if not inquiry:
            raise exceptions.NotFound(_("Inquiry not found"))
        if inquiry.user != user:
            raise exceptions.PermissionDenied(
                _("You are not allowed to answer this inquiry")
            )
        return True

    def get_queryset(self):
        inquiry_id = self.kwargs.get("id")
        if self.request.user.role == "admin":
            return self.queryset.filter(inquiry_id=inquiry_id)
        return self.queryset.filter(
            inquiry_id=inquiry_id, inquiry__user=self.request.user
        )

    def perform_create(self, serializer):
        return serializer.save(inquiry_id=self.kwargs.get("id"), user=self.request.user)

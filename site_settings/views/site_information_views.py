from rest_framework import response, viewsets

from authentications.models import User
from site_settings.models import SiteInformation
from site_settings.serializers import SiteInformationSerializer
from utils.extensions.permissions import IsAdminOrReadOnly


class SiteInformationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing site information.
    Only admin has access to this viewset.
    He can view and edit site information.
    There can be only one item in this model, which will be created with this viewset. That means only first item will be created.
    Multiple item is not allowed.
    Also that item can not be deleted.
    There won't be any list view for this model.
    On the base api where normally list view is shown, there will be only one item shown, which will be the first item.
    There won't be any specific retrieve view for this model. Retrieval of the first item will be based on the base api.
    """

    queryset = SiteInformation.objects.all()
    serializer_class = SiteInformationSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ["get", "post", "head", "options"]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset.first())
        return response.Response(serializer.data)


class DashboardViewSet(viewsets.ViewSet):
    """
    A viewset for viewing dashboard information.
    Only admin has access to this viewset.
    He can view dashboard information.
    """

    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ["get", "head", "options"]

    def list(self, request):
        # course = Course.objects.all().prefetch_related(
        #     "enrollments", "reviews", "course_progresses"
        # )
        #
        # avg_review = 0
        # total_review = 0
        # total_rating = 0
        # avg_course_progress_rate = 0
        # total_course_progress_rate = 0
        #
        # for c in course:
        #     review = c.reviews.all()
        #     total_review += review.count()
        #     for r in review:
        #         total_rating += r.rating
        #     course_progress = c.course_progresses.all()
        #     for cp in course_progress:
        #         total_course_progress_rate += cp.progress
        #
        # if total_review:
        #     avg_review = total_rating / total_review
        #
        # if total_course_progress_rate:
        #     avg_course_progress_rate = total_course_progress_rate / course.count()
        #
        # data = {
        #     "number_of_students": User.objects.filter(role="student").count(),
        #     "average_course_progress_rate": avg_course_progress_rate,
        #     "average_course_rating": avg_review,
        #     "community_question_count": Community.objects.all().count(),
        # }
        return response.Response("data")

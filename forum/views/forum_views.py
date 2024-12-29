from django.db import transaction
from django.db.models import Prefetch
from rest_framework import (
    filters,
    generics,
    permissions,
    response,
    status,
    views,
    viewsets,
)

from forum.models import Forum, ForumComment, ForumLike, Tag
from forum.serializers import (
    ForumCommentsSerializer,
    ForumDetailSerializer,
    ForumListSerializer,
    TagCreateSerializer,
    TagSerializer,
)
from utils.extensions.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class TagView(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            if self.request.user.is_superuser or self.request.user.is_staff:
                return TagCreateSerializer
            return TagSerializer
        else:
            return TagCreateSerializer


class ForumViewSets(viewsets.ModelViewSet):
    queryset = (
        Forum.objects.all()
        .select_related("user__user_information", "province", "city")
        .prefetch_related(
            "images",
            "tags",
            Prefetch(
                "forum_comments",
                queryset=ForumComment.objects.filter(
                    parent_comment=None
                ).prefetch_related("replies__replies__replies__replies__replies"),
            ),
        )
    ).order_by("-created_at")
    lookup_field = "slug"
    filterset_fields = ("tags",)
    ordering_fields = ("total_like", "created_at")
    search_fields = ["title"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            user_likes = ForumLike.objects.filter(user=self.request.user).values_list(
                "forum_id", flat=True
            )
            context["user_likes"] = set(user_likes)
        else:
            context["user_likes"] = set()
        return context

    def get_serializer_class(self):
        if self.action == "list":
            return ForumListSerializer
        return ForumDetailSerializer

    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ForumLikeView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def toggle_like(self, user):
        forum = generics.get_object_or_404(Forum, slug=self.kwargs.get("slug"))
        like, created = ForumLike.objects.get_or_create(forum=forum, user=user)
        if created:
            forum.total_like += 1
            data = "Liked"
        else:
            like.delete()
            forum.total_like -= 1
            data = "Disliked"
        forum.save(update_fields=["total_like"])  # Update only 'total_like'
        return data

    def get(self, request, *args, **kwargs):
        data = self.toggle_like(request.user)
        return response.Response({"data": data}, status=status.HTTP_200_OK)


class ForumCommentView(generics.ListCreateAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ForumCommentsSerializer

    def get_queryset(self):
        return (
            ForumComment.objects.filter(
                forum__slug=self.kwargs.get("slug"), parent_comment=None
            )
            .prefetch_related("replies__replies__replies__replies__replies")
            .select_related("user__user_information")
        )

    @transaction.atomic()
    def perform_create(self, serializer):
        forum = Forum.objects.get(slug=self.kwargs.get("slug"))
        forum.total_comment += 1
        forum.save(update_fields=["total_comment"])

        serializer.save(
            forum=forum,
            user=self.request.user,
        )

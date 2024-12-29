from django.db import transaction
from django.db.models import Exists, F, OuterRef, Prefetch
from rest_framework import (
    filters,
    generics,
    permissions,
    response,
    status,
    views,
    viewsets,
)

from article.models import Article, ArticleCategory, ArticleComment, ArticleLike
from article.serializers import (
    ArticleCategoryCreateSerializer,
    ArticleCategorySerializer,
    ArticleCommentsSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
)
from utils.extensions.permissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrReadOnly


class ArticleCategoryView(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = ArticleCategory.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            if self.request.user.is_superuser or self.request.user.is_staff:
                return ArticleCategoryCreateSerializer
            return ArticleCategorySerializer
        else:
            return ArticleCategoryCreateSerializer

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return response.Response(
            {"data": "Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class ArticleView(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrReadOnly,
    )
    queryset = (
        Article.objects.all()
        .select_related("user__user_information", "category")
        .prefetch_related(
            Prefetch(
                "article_comments",
                queryset=ArticleComment.objects.filter(
                    parent_comment=None
                ).prefetch_related("replies__replies__replies__replies__replies"),
            ),
        )
    )
    lookup_field = "slug"
    filterset_fields = ("category",)
    ordering_fields = ("total_like",)
    search_fields = ["title"]

    def get_queryset(self):
        return self.queryset.annotate(
            is_liked=Exists(
                ArticleLike.objects.filter(
                    article_id=OuterRef("id"), user=self.request.user
                )
            )
        ).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return ArticleListSerializer
        if self.action == "retrieve":
            return ArticleDetailSerializer
        return ArticleDetailSerializer  # I don't know what you want for create/destroy/update.

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleLikeView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def toggle_like(self, user):
        article = generics.get_object_or_404(Article, slug=self.kwargs.get("slug"))
        like, created = ArticleLike.objects.get_or_create(article=article, user=user)
        if created:
            article.total_like += 1
            data = "Liked"
        else:
            like.delete()
            article.total_like -= 1
            data = "Disliked"
        article.save(update_fields=["total_like"])  # Update only 'total_like'
        return data

    def get(self, request, *args, **kwargs):
        data = self.toggle_like(request.user)
        return response.Response({"data": data}, status=status.HTTP_200_OK)


class ArticleCommentView(generics.ListCreateAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ArticleCommentsSerializer

    def get_queryset(self):
        return (
            ArticleComment.objects.filter(
                article__slug=self.kwargs.get("slug"), parent_comment=None
            )
            .prefetch_related("replies__replies__replies__replies__replies")
            .select_related("user__user_information")
        )

    @transaction.atomic()
    def perform_create(self, serializer):
        article = Article.objects.get(slug=self.kwargs.get("slug"))
        article.total_comment += 1
        article.save(update_fields=["total_comment"])

        serializer.save(
            article=article,
            user=self.request.user,
        )

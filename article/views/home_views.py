from django.db.models import Prefetch
from rest_framework import generics, permissions, response, status, views

from article.models import Article, ArticleCategory
from article.serializers import HomeArticleCategorySerializer
from forum.models import Forum, Tag


class HomePageView(generics.ListAPIView):
    serializer_class = HomeArticleCategorySerializer
    queryset = ArticleCategory.objects.all().prefetch_related(
        Prefetch(
            "article_category",
            queryset=Article.objects.all().select_related(
                "user__user_information", "category"
            ),
        )
    )
    permission_classes = (permissions.IsAuthenticated,)

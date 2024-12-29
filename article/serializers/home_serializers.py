from rest_framework import serializers

from article.models import ArticleCategory
from article.serializers import ArticleListSerializer


class HomeArticleCategorySerializer(serializers.ModelSerializer):
    articles = ArticleListSerializer(
        many=True, read_only=True, source="article_category"
    )

    class Meta:
        model = ArticleCategory
        fields = ("id", "name", "icon", "articles")

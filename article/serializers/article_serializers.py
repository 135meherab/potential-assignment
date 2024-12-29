from rest_framework import serializers

from article.models import Article, ArticleCategory, ArticleComment
from authentications.serializers import BasicUserInformationSerializer


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ("id", "icon", "name")


class ArticleCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ("id", "icon", "name_en", "name_ko")


class ArticleCommentsSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    user = BasicUserInformationSerializer(read_only=True)

    class Meta:
        model = ArticleComment
        fields = (
            "id",
            "user",
            "content",
            "image",
            "created_at",
            "replies",
            "parent_comment",
        )
        # write_only_fields = ("article", "parent_comment",)
        extra_kwargs = {
            # "article": {"write_only": True},
            "parent_comment": {"write_only": True},
            # "user": {"read_only": True},
        }

    def get_replies(self, obj):
        # Get all replies for the current comment
        replies = obj.replies.all()
        return ArticleCommentsSerializer(
            replies, many=True, context={"request": self.context.get("request")}
        ).data

    def validate_parent_comment(self, value):
        if value:
            article_slug = self.context.get("view").kwargs.get("slug")
            if value.article.slug != article_slug:
                raise serializers.ValidationError("Must belong to the same article.")

        return value


class ArticleListSerializer(serializers.ModelSerializer):
    user = BasicUserInformationSerializer(read_only=True)
    category = ArticleCategorySerializer(read_only=True)
    is_liked = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = Article
        fields = [
            "id",
            "slug",
            "title",
            "short_content",
            "category",
            "user",
            "total_like",
            "total_comment",
            "thumbnail",
            "created_at",
            "updated_at",
            "is_liked",
        ]


class ArticleDetailSerializer(ArticleListSerializer):
    article_comments = ArticleCommentsSerializer(many=True, read_only=True)

    class Meta(ArticleListSerializer.Meta):
        fields = ArticleListSerializer.Meta.fields + ["content", "article_comments"]

from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.db import models
from tinymce.models import HTMLField

from core.models import BaseModel, CompressedImageField
from utils.helper import content_file_path

# Create your models here.


class ArticleCategory(BaseModel):
    name = models.CharField(max_length=100, blank=True)
    icon = CompressedImageField(quality=75, width=1920)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return self.name


class Article(BaseModel):
    slug = AutoSlugField(populate_from="title", unique=True)
    title = models.CharField(max_length=100)
    thumbnail = CompressedImageField(quality=75, width=1920, blank=True, null=True)
    short_content = models.TextField()
    content = HTMLField()
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.PROTECT,
        related_name="articles",
    )
    user = models.ForeignKey(
        "authentications.User",
        on_delete=models.PROTECT,
        related_name="articles",
        verbose_name="Article Author",
    )
    total_like = models.PositiveIntegerField(default=0, editable=False)
    total_comment = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title


class ArticleComment(BaseModel):
    content = models.TextField()
    image = CompressedImageField(quality=75, width=1920, blank=True, null=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_comments"
    )
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        "authentications.User",
        on_delete=models.PROTECT,
        related_name="article_comments",
        verbose_name="Comment by",
    )

    def clean(self):
        errors = {}
        # Ensure that the parent comment belongs to the same article
        if self.parent_comment and self.parent_comment.article_id != self.article_id:
            errors.setdefault("parent_comment", []).append(
                "Parent comment must belong to the same article."
            )

        if errors:
            raise ValidationError(errors)

    def get_replies(self):
        return ArticleComment.objects.filter(comment=self)

    def __str__(self):
        return f"Comment by {self.user.user_information.full_name} on {self.article}"


class ArticleLike(BaseModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_like"
    )
    user = models.ForeignKey(
        "authentications.User",
        on_delete=models.PROTECT,
        related_name="article_likes",
        verbose_name="Liked by",
    )

    class Meta:
        unique_together = (("article", "user"),)

    def __str__(self):
        return f"{self.user.user_information.full_name} like {self.article}"

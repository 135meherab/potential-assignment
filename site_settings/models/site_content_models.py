from django.db import models

from core.models import BaseModel, CompressedImageField
from utils.helper import content_file_path


class Banner(BaseModel):
    user = models.ForeignKey(
        "authentications.User",
        on_delete=models.CASCADE,
        related_name="banners",
        verbose_name="Banner Creator",
        help_text="User who created the banner",
    )
    short_text = models.CharField(max_length=255)
    long_text = models.CharField(max_length=255)
    background_color = models.CharField(max_length=8)
    image = CompressedImageField(quality=75, width=1920)
    link = models.URLField(blank=True, null=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.short_text


class FAQ(BaseModel):
    user = models.ForeignKey(
        "authentications.User",
        on_delete=models.CASCADE,
        related_name="faqs",
        verbose_name="FAQ Creator",
        help_text="User who created the FAQ",
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "FAQs"

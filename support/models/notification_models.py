from django.db import models

from core.models import BaseModel


class Notification(BaseModel):
    user = models.ForeignKey(
        "authentications.User", on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.title}"

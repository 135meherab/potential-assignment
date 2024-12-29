from django.db.models.signals import post_save
from django.dispatch import receiver

from article.models import ArticleComment
from support.models import Notification


@receiver(post_save, sender=ArticleComment)
def create_article_comment_instance(sender, instance, created, **kwargs):
    if created:
        if instance.parent_comment:
            Notification.objects.create(
                user=instance.parent_comment.user,
                title="New Reply",
                body=f"{instance.user.user_information.full_name} replied to your comment.",
            )

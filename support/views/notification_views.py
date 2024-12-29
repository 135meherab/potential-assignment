from rest_framework import generics, permissions

from support.models import Notification
from support.serializers import NotificationSerializers


class NotificationView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotificationSerializers

    def get_queryset(self):
        # return Notification.objects.filter(user=self.request.user)

        # Get all notifications for the current user
        notifications = Notification.objects.filter(user=self.request.user)

        # Mark notifications as read if the user visits this page
        notifications.update(is_read=True)

        return notifications

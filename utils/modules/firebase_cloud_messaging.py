# from fcm_django.models import FCMDevice
# from firebase_admin.messaging import Message, Notification
# from django.shortcuts import get_object_or_404, get_list_or_404
#
#
# class FCMNotificationSender:
#     @classmethod
#     def send_single_notification(self, title, body, image=None):
#         try:
#             device = FCMDevice.objects.all().first()  # Get any device for demonstration
#             # general send_message method
#             message = self.generate_message(title, body, image)
#             device.send_message(message)
#             return True
#         except FCMDevice.DoesNotExist:
#             print("Device does not exist.")
#             return False
#         except Exception as e:
#             print(f"An error occurred while sending notification: {e}")
#             return False
#
#     @classmethod
#     def send_group_notification(self, title, body, image=None):
#         try:
#             devices = FCMDevice.objects.all()
#             # general send_message method
#             message = self.generate_message(title, body, image)
#             devices.send_message(message)
#             # Or (send_message parameters include: messages, dry_run, app)
#             FCMDevice.objects.send_message(Message(...))
#             return True
#         except Exception as e:
#             print(f"An error occurred while sending group notification: {e}")
#             return False
#
#     @staticmethod
#     def subscribing_topic(topic=None, tokens=None):
#         if tokens is None:
#             raise ValueError("Tokens cannot be None")
#         if topic:
#             try:
#                 device_list = get_list_or_404(FCMDevice, registration_id=tokens)
#                 device_list.handle_topic_subscription(True, topic=topic)
#             except FCMDevice.DoesNotExist:
#                 print("Device with ID  does not exist.")
#                 return False
#             except Exception as e:
#                 print(f"An error occurred while subscribing to a topic: {e}")
#                 return False
#         return False
#
#     @staticmethod
#     def Unsubscribing_topic(topic=None, tokens=None):
#         if tokens is None:
#             raise ValueError("Tokens cannot be None")
#         try:
#             device = get_object_or_404(FCMDevice, registration_id=tokens)
#             device.handle_topic_subscription(False, topic=topic)
#             return True
#         except FCMDevice.DoesNotExist:
#             print("Device with ID  does not exist.")
#             return False
#         except Exception as e:
#             print(f"An error occurred while unsubscribing to a topic: {e}")
#             return False
#
#     @classmethod
#     def send_message_with_topic(self, title, body, image=None, topic=None):
#         """
#         send message with specific topic to all devices subscribed to that topic
#         """
#         try:
#             message = self.generate_message(title, body, image)
#             FCMDevice.send_topic_message(message, topic=topic)
#             return True
#         except Exception as e:
#             print(f"An error occurred while sending message with topic: {e}")
#             return False
#
#     @staticmethod
#     def generate_message(title=None, body=None, image=None):
#         """
#         generate message body for fcm notification
#         """
#         return Message(
#             notification=Notification(title=title, body=body, image=image)
#         )

from django.shortcuts import get_list_or_404, get_object_or_404
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


class FCMNotificationSender:
    title: str
    body: str
    image: str
    tokens = list[str]
    topic: str

    def __init__(self, title=None, body=None, image=None, tokens=None, topic=""):
        self.title = title
        self.body = body
        self.image = image
        self.token = tokens
        self.topic = topic

    def send_single_notification(self):
        try:
            if device := FCMDevice.objects.first():
                message = self.generate_message()
                device.send_message(message)
                return True
            else:
                print("No devices registered.")
                raise FCMDevice.DoesNotExist
        except Exception as e:
            print(f"An error occurred while sending notification: {e}")
            raise Exception(e)

    def send_group_notification(self):
        try:
            if devices := FCMDevice.objects.all():
                message = self.generate_message()
                devices.send_message(message)
                return True
            else:
                print("No devices registered.")

                raise FCMDevice.DoesNotExist
        except Exception as e:
            print(f"An error occurred while sending group notification: {e}")
            raise Exception(e)

    def subscribing_topic(self):
        if self.tokens is None:
            raise ValueError("Tokens cannot be None")
        try:
            device_list = get_list_or_404(FCMDevice, registration_id=self.tokens)
            for device in device_list:
                device.handle_topic_subscription(True, topic=self.topic)
            return True
        except Exception as e:
            print(f"An error occurred while subscribing to a topic: {e}")
            return False

    def unsubscribing_topic(self):
        if self.tokens is None:
            raise ValueError("Tokens cannot be None")
        try:
            device = get_object_or_404(FCMDevice, registration_id=self.tokens)
            device.handle_topic_subscription(False, topic=self.topic)
            return True
        except Exception as e:
            print(f"An error occurred while unsubscribing to a topic: {e}")
            return False

    def send_message_with_topic(self):
        try:
            message = self.generate_message()
            FCMDevice.send_topic_message(message, topic=self.topic)
            return True
        except Exception as e:
            print(f"An error occurred while sending message with topic: {e}")
            return False

    def generate_message(self):
        return Message(
            notification=Notification(
                title=self.title, body=self.body, image=self.image
            )
        )

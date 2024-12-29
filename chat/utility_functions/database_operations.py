#  get group informations
from channels.db import database_sync_to_async
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from chat.models import ChatLog, ChatSession


@database_sync_to_async
def get_chat_session(room_id, participant: list = None):
    chat_session, created = ChatSession.objects.get_or_create(room_id=room_id)
    if participant:
        chat_session.participants.add(*participant)
    return chat_session, created


@database_sync_to_async
def get_chat_session_history(room_id, page_number=1, page_size=20):
    try:
        chat_session = ChatSession.objects.prefetch_related(
            "chat_messages_session", "chat_messages_session__user"
        ).get(room_id=room_id)
        chat_logs = chat_session.chat_messages_session.all()

        # Paginate the query results
        paginator = Paginator(chat_logs, page_size)
        try:
            paginated_logs = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_logs = paginator.page(1)
        except EmptyPage:
            paginated_logs = paginator.page(paginator.num_pages)

        return paginated_logs.object_list
    except ChatSession.DoesNotExist:
        return []


@database_sync_to_async
def store_chat_message(room_id, user, message):
    chat_session = ChatSession.objects.get(room_id=room_id)
    return ChatLog.objects.create(room=chat_session, user=user, content=message)

from channels.db import database_sync_to_async


@database_sync_to_async
def chat_history_modifier(chat_logs):
    response = []
    for chat_log in chat_logs:
        response.append(
            {
                "id": chat_log.id,
                "user": chat_log.user.user_information.full_name,
                "message": chat_log.content,
            }
        )
    return response

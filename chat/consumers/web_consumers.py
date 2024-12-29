import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.utility_functions.database_operations import (
    get_chat_session,
    get_chat_session_history,
    store_chat_message,
)
from chat.utility_functions.database_response_modifier import chat_history_modifier


class AsyncWebConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        key = self.scope["url_route"]["kwargs"]["key"]
        self.group_name = key
        chat_session, new = await get_chat_session(key, [user])
        if chat_session:
            #  add channels group
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            chat_history = await get_chat_session_history(chat_session.room_id)
            response = await chat_history_modifier(chat_history)
            # send connected message
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "send_message", "status": "Connected", "data": response},
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        chat_log = await store_chat_message(
            self.group_name, self.scope["user"], content["message"]
        )
        response = {
            "id": chat_log.id,
            "user": chat_log.user.username,
            "message": chat_log.content,
        }
        await self.channel_layer.group_send(
            self.group_name, {"type": "send_message", "data": response}
        )

    #  sent message to the group
    async def send_message(self, event):
        await self.send(text_data=json.dumps(event))

import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        connected_user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        self.user_id = self.scope["user"].id
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": text_data,
                "user_id": str(self.user_id)}
        )

    # Receive message from room group
    async def chat_message(self, event):
        connected_user_model = self.scope["user"]
        message = event["message"]
        user_id = str(connected_user_model.id)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "user_id": user_id}))


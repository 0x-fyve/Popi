from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f"room_{room_name}"

        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

    async def receive(self, text_data):

        data = json.loads(text_data)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                "message": data
            }
        )

    async def chat_message(self, event):
        json_message = json.dumps(event["message"])
        await self.send(json_message)

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )    
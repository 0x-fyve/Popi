from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .middleware import get_room
    
class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_code = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f"room_{room_code}"

        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close()
            return

        room = await get_room(room_code)

        if not room:
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
        message = json.dumps(event["message"])
        await self.send(message)

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )    
from channels.generic.websocket import AsyncWebsocketConsumer

class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        
        room_name = self.scope['url_route']['kwargs']['room_name']

        self.group_name = f'room_{room_name}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()


    async def receive(self, text_data):

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                "message": text_data
            }
        )

    async def chat_message(self, event):
        await self.send(event["message"])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
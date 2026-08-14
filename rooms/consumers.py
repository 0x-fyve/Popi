from channels.generic.websocket import AsyncWebsocketConsumer

class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        room_name = self.scope['url_route']['kwargs']['room_name']

        group_name = f'room_{room_name}'

    async def receive(self, text_data):
        await self.send(text_data=text_data)

    def disconnect(self, close_code):
        pass        
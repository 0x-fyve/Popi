from channels.generic.websocket import AsyncWebsocketConsumer

class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        
        room_name = self.scope['url_route']['kwargs']['room_name']

        group_name = f'room_{room_name}'

        await self.channel_layer.group_add(group_name, self.channel_name)

        await self.accept()


    async def receive(self, text_data):
        pass

    def disconnect(self, close_code):
        pass        
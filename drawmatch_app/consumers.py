from typing import Any

from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json


class DrawConsumer(AsyncJsonWebsocketConsumer):
    room_code: str = None
    room_group_name: str = None

    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'room_{self.room_code}'
        print(f"room_code: {self.room_code}")
        print(f"room_group_name: {self.room_group_name}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data: str = None, _: Any = None) -> None:
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'draw',
                'data': data
            }
        )

    async def send_message(self, res):
        await self.send(text_data=json.dumps({
            "payload": res
        }))

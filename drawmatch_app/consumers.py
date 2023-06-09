import json
from typing import Any

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from drawmatch_app.models import ActiveRooms, Users


class DrawConsumer(AsyncJsonWebsocketConsumer):
    room_code: str = None
    room_group_name: str = None

    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'room_{self.room_code}'

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

    # Receive message from WebSocket
    async def receive(self, text_data: str = None, _: Any = None) -> None:
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': data['type'],
                'data': data
            }
        )

    # Receive message from room group
    async def draw(self, event):
        await self.send(text_data=json.dumps({
            'payload': event['data']
        }))

    async def erase(self, event):
        await self.send(text_data=json.dumps({
            'payload': event['data']
        }))

    async def score(self, event):
        await self.send(text_data=json.dumps({
            'payload': event['data']
        }))

    async def word(self, event):
        await self.send(text_data=json.dumps({
            'payload': event['data']
        }))


class UserJoinedConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.id_user_right = None
        self.name_user_right = None
        self.room = None
        super().__init__(*args, **kwargs)

    async def user_joined(self, event):
        user_id = event['user_id']
        user_name = event['user_name']
        self.id_user_right = user_id
        self.name_user_right = user_name
        await self.send_json({
            'id_user_right': self.id_user_right,
            'name_user_right': self.name_user_right
        })

    async def websocket_connect(self, event):
        room_code = self.scope['url_route']['kwargs']['room_code']
        self.room = await sync_to_async(ActiveRooms.objects.get)(pk=room_code)
        await self.channel_layer.group_add(
            room_code,
            self.channel_name
        )
        await self.accept()

        if self.room.id_user_right_id is not None:
            user_id = self.room.id_user_right_id
            right_user = await sync_to_async(Users.objects.get)(pk=self.room.id_user_right_id)
            user_name = right_user.name
            await self.channel_layer.group_send(
                room_code,
                {
                    'type': 'user_joined',
                    'user_id': user_id,
                    'user_name': user_name
                }
            )

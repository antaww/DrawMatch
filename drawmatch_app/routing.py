from drawmatch_app.consumers import DrawConsumer, UserJoinedConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/room/<room_code>/', DrawConsumer.as_asgi()),
    path('ws/userjoined/<room_code>/', UserJoinedConsumer.as_asgi()),
]

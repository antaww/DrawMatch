from drawmatch_app.consumers import DrawConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/room/<room_code>/', DrawConsumer.as_asgi()),
]

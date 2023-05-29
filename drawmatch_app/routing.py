from django.template.defaulttags import url

from drawmatch_app.consumers import DrawConsumer

websocket_urlpatterns = [
    url(r'^ws/room/(?P<room_code>\w+)/$', DrawConsumer.as_asgi()),
]

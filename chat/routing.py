from .consumers import ChatConsumer
from django.urls import re_path
websocket_urlpatterns = [
    re_path(r'ws/rooms/(?P<room_id>\d+)/$', ChatConsumer.as_asgi()),
]
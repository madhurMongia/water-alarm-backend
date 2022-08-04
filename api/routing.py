from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/current_level/<int:pk>/',
         consumers.CurrentLevelConsumer.as_asgi()),
]

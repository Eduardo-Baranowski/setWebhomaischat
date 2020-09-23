from django.conf.urls import url
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    url(r"^ws/callback/(?P<uuid>[^/]+)/$", consumers.WebhookConsumer),
    #url(r"^ws/callback/(?P<uuid>[^/]+)/$", consumers.WebhookConsumer),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]

import os   #

from channels.routing import ProtocolTypeRouter, URLRouter #
from django.core.asgi import get_asgi_application   #

import mainapp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  #


from channels.auth import AuthMiddlewareStack   #
from mainapp.routing import websocket_urlpatterns   #

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
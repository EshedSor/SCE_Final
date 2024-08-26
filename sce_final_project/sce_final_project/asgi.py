"""
ASGI config for sce_final_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import communications.routing  # Import the routing module
import notifications.routing
from communications.middlewares import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sce_final_project.settings')
websocket_urlpatterns = communications.routing.websocket_urlpatterns + notifications.routing.websocket_urlpatterns

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
        websocket_urlpatterns  # Use the correct import path
        )
    ),
})

print("websocket_urlpatterns in asgi.py:", communications.routing.websocket_urlpatterns)
print("websocket_urlpatterns in asgi.py:", notifications.routing.websocket_urlpatterns)
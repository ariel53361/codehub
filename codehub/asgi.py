import os
import django

# Set the settings module and initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codehub.settings.dev')
django.setup()  # This ensures settings and apps are fully loaded

# Now safe to import Django-related modules
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

print("Loading ASGI application")
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
"""
ASGI config for ushiku project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
#from channels.routing import ProtocolTypeRouter, URLRouter
#from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

#import same application as asgi
#import sagyoshiji.routing
#import sagyodenpyo.routing
#import home.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ushiku.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            #sagyoshiji.routing.websocket_urlpatterns +
            #sagyodenpyo.touting.websocket_urlpatterns +
            #home.routing.websocket_urlpatterns
            
        )
    )
})
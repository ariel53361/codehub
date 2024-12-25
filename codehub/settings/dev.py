import os
from .common import *

DEBUG = True

SECRET_KEY = "django-insecure-c0%n3r)(1coucuk!k4h4w2q*)&syz8n854fa=b*+2ezpjpf8j0"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'codehub',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'USER': 'root',
    }
}

SIMPLE_JWT = {
    **SIMPLE_JWT,  
    'AUTH_COOKIE_SECURE': False,
}

MIDDLEWARE.insert(2, 'debug_toolbar.middleware.DebugToolbarMiddleware')
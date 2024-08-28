import os
from .common import *

DEBUG = True

SECRET_KEY = "django-insecure-c0%n3r)(1coucuk!k4h4w2q*)&syz8n854fa=b*+2ezpjpf8j0"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'codehub',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '1234'
    }
}
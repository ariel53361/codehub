import os
from urllib.parse import urlparse
from .common import *
from decouple import config

DEBUG = False

SECRET_KEY = config('SECRET_KEY')

DATABASE_URL = config('DATABASE_URL')
url = urlparse(DATABASE_URL)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
    }
}

SIMPLE_JWT = {
    **SIMPLE_JWT,
    'AUTH_COOKIE_SECURE': True,
}

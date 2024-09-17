import os
from urllib.parse import urlparse
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

DATABASE_URL = os.getenv('DATABASE_URL')
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

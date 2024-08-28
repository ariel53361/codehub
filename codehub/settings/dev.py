import os
from .common import *

DEBUG = True

SECRET_KEY = "2%!)6(ib=@0b7j1xi)!rmzl6n_1ven#wb$=0a3vs#m)n$&*=5#"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'codehub',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '1234'
    }
}
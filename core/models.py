from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, error_messages={
                              'unique': 'A user with this email already exists.'})

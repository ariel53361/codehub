from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to='avatars', default='avatars/default_avatar.svg', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.pk}-{self.get_full_name()}'


class Topic(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, null=True, related_name='rooms')
    subject = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.topic}-{self.subject}'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.get_full_name()}-{self.room.subject}'

import uuid
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from codehub.settings import common


class Profile(models.Model):
    user = models.OneToOneField(
        common.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    avatar = models.ImageField(
        upload_to='avatars', default='avatars/default_avatar.svg', null=True, blank=True)

    bio = models.TextField(blank=True, default='')

    def __str__(self) -> str:
        return f'{self.user.first_name}-{self.user.last_name}'


class Topic(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    host = models.ForeignKey(Profile, on_delete=models.CASCADE)
    topic = models.ForeignKey(
        Topic, on_delete=models.PROTECT, related_name='rooms')
    subject = models.CharField(max_length=200, validators=[
                               MinLengthValidator(2)])
    description = models.TextField(null=True, blank=True, max_length=200)
    participants = models.ManyToManyField(
        Profile, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.topic}-{self.subject}'


class Message(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "profile", "client_id"],
                name="uniq_message_client_id_per_sender_room",
            )
        ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    client_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(validators=[
        MinLengthValidator(2, "Message must be at least 2 characters"),
        MaxLengthValidator(50000, "Message cannot exceed 50,000 characters")
    ])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.profile}-{self.room.subject}'

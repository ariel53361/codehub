from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import Profile, Topic, Room, Message


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    avatar = serializers.ImageField(required=False, allow_null=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.avatar:
            ret['avatar'] = instance.avatar.name.split('/')[-1]
        return ret

    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'avatar', 'bio']

    # def update(self, instance, validated_data):
    #     password = validated_data.pop('password', None)
    #     if password:
    #         instance.set_password(password)

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()
    #     return instance


class TopicSerializer(serializers.ModelSerializer):
    room_num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'room_num']


class RoomSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()
    host = ProfileSerializer()
    participants = ProfileSerializer(many=True, read_only=True)
    participants_num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'topic', 'subject', 'description', 'host', 'participants', 'participants_num',
                  'updated', 'created']


class SimpleRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'topic', 'subject']


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'topic', 'subject', 'description']

    def create(self, validated_data):
        user = self.context['user']

        profile = Profile.objects.get(user=user)
        return Room.objects.create(
            host=profile, **validated_data)


class MessageSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    room = SimpleRoomSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'profile', 'content', 'room', 'updated', 'created']

    def save(self, **kwargs):
        user_id = self.context['user_id']
        room = Room.objects.get(pk=self.context['room_id'])

        profile = Profile.objects.get(user__id=user_id)
        self.instance = Message.objects.create(
            user=profile, room=room, **self.validated_data)
        if room.host != profile:
            room.participants.add(profile)

        return self.instance

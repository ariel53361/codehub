from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import User, Topic, Room, Message


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    avatar = serializers.ImageField(required=False)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'first_name',
                  'last_name', 'avatar', 'is_active', 'email', 'date_joined']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        avatar = validated_data.pop('avatar', None)
        instance.avatar = avatar

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email',
                  'first_name', 'last_name', 'avatar']


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']


class TopicSerializer(serializers.ModelSerializer):
    room_num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'room_num']


class RoomSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()
    host = SimpleUserSerializer()
    participants = SimpleUserSerializer(many=True, read_only=True)
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
    topic = TopicSerializer()

    class Meta:
        model = Room
        fields = ['topic', 'subject', 'description']

    def create(self, validated_data):
        print('create')
        user_id = self.context['user_id']
        topic = Topic.objects.get(name=validated_data.get('topic')['name'])

        if not topic:
            raise serializers.ValidationError(
                {'topic': 'This topic does not existes'})

        user = User.objects.get(pk=user_id)
        return Room.objects.create(
            host=user, topic=topic, subject=validated_data['subject'], description=validated_data['description'])

    # def create(self, validated_data):
    #     user_id = self.context.get('user_id')
    #     topic_id = self.context.get('topic_id')
    #     print(topic_id)
    #     if not topic_id or not Topic.objects.filter(pk=topic_id).exists():
    #         raise serializers.ValidationError("Invalid topic_id or topic does not exist.")
    #     user = User.objects.get(pk=user_id)
    #     topic = Topic.objects.get(pk=topic_id)
    #     return Room.objects.create(host=user, topic=topic, **validated_data)


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = SimpleRoomSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'room', 'updated', 'created']

    def save(self, **kwargs):
        user_id = self.context['user_id']
        room = Room.objects.get(pk=self.context['room_id'])

        try:
            user = User.objects.get(pk=user_id)
            self.instance = Message.objects.create(
                user=user, room=room, **self.validated_data)
            if room.host != user:
                room.participants.add(user)

        except:
            # heandle update message
            pass
            # message = Message(user_pk=user_id)
            # message.content = self.validated_data['content']
            # self.instance = message

        return self.instance


# class CreateOrUpdateMessageSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Message
#         fields = ['id', 'user', 'content', 'room', 'updated', 'created']

#     def save(self, **kwargs):
#         user_id = self.context['user_id']
#         room = Room.objects.get(pk=self.context['room_id'])

#         try:
#             message = Message(user_pk=user_id)
#             message.content = self.validated_data['content']
#             self.instance = message
#         except:
#             user = User.objects.get(pk=user_id)
#             self.instance = Message.objects.create(
#                 user=user, room=room, **self.validated_data)

#         return self.instance

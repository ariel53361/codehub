from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from chat.filters import RoomFilter
from chat.permissions import IsMessageWriter, IsCurrentUser
from django.db.models.aggregates import Count, Max
from .models import Profile, Topic, Message, Room
from .serializers import CreateRoomSerializer, ProfileSerializer, TopicSerializer, MessageSerializer, RoomSerializer
from django.contrib.auth import get_user_model


@api_view(["GET"])
def test_email_view(request):
    # send_mail("subject", "message", "ariel53361@gmail.com",
    #           ["ariel53361@gmail.com"])
    User = get_user_model()
    User.objects.filter(id__gte=38).delete()

    return Response({
        "success":  1,
    })


class ProfileViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Profile.objects.all()
    http_method_names = ['get', 'patch', 'head', 'options']
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        if self.request.method in ['PATCH']:
            return [IsCurrentUser()]
        return [AllowAny()]

    @action(detail=False, methods=['GET', 'PATCH'])
    def me(self, request):
        (proflie, created) = Profile.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = ProfileSerializer(proflie)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = ProfileSerializer(
                proflie, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class TopicViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = TopicSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        topic_pk = self.kwargs.get('pk')
        base_queryset = Topic.objects.annotate(
            room_num=Count('rooms')).order_by('name')
        if topic_pk:
            return base_queryset.filter(pk=topic_pk)
        return base_queryset


class RoomViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    http_method_names = ['get', 'post', 'destroy', 'head', 'options']
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RoomFilter
    ordering_fields = ['created', 'participants_num', 'last_activity']

    def get_queryset(self):
        room_pk = self.kwargs.get('pk')
        base_queryset = Room.objects\
            .select_related('host', 'topic')\
            .prefetch_related('participants', 'messages')\
            .annotate(participants_num=Count('participants', distinct=True))\
            .annotate(last_activity=Max('messages__created'))\
            .order_by('-last_activity')
        if room_pk:
            return base_queryset.filter(pk=room_pk)
        return base_queryset

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return CreateRoomSerializer
        return RoomSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_context(self):
        topic_pk = self.kwargs.get('topic_id')
        if topic_pk:
            return {'user': self.request.user,
                    'topic_id': self.kwargs['topic_id']}
        return {'user': self.request.user}


class MessageViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    http_method_names = ['get', 'head', 'options']
    serializer_class = MessageSerializer

    def get_serializer_context(self):
        room_pk = get_object_or_404(Room, pk=self.kwargs['room_pk']).id
        return {'user_id': self.request.user.id, 'room_id': room_pk}

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        room_pk = self.kwargs.get('room_pk')
        if room_pk:
            return Message.objects.filter(room_id=room_pk).select_related('profile').order_by('-created')
        return Message.objects.all().select_related('profile', 'room').order_by('-created')

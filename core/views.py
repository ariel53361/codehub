from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.filters import RoomFilter
from core.permissions import IsMessageWriter, IsCurrentUser
from django.db.models.aggregates import Count, Max
from .models import User, Topic, Message, Room
from .serializers import CreateRoomSerializer, UserSerializer, TopicSerializer, MessageSerializer, RoomSerializer


class UserViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH']:
            return [IsCurrentUser()]
        return [AllowAny()]


class TopicViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = TopicSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        topic_pk = self.kwargs.get('pk')
        self.get_object
        base_queryset = Topic.objects.annotate(room_num=Count('rooms'))
        if topic_pk:
            return base_queryset.filter(pk=topic_pk)
        return base_queryset

    # def get_permissions(self):
    #     if self.request.method in ['POST', 'DELETE']:
    #         return [IsAdminUser()]
    #     return [AllowAny()]


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
            .annotate(participants_num=Count('participants', distinct=True)).annotate(last_activity=Max('messages__created')).order_by('-last_activity')
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
            return {'user_id': self.request.user.id,
                    'topic_id': self.kwargs['topic_id']}
        return {'user_id': self.request.user.id}


class MessageViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,  mixins.CreateModelMixin, mixins.DestroyModelMixin):
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']
    pagination_class = None
    serializer_class = MessageSerializer

    def get_serializer_context(self):
        room_pk = self.kwargs.get('room_pk')
        if room_pk:
            return {'user_id': self.request.user.id, 'room_id': self.kwargs['room_pk']}
        return {}

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        # for some reason the IsMessageWriter permission is not workin with the PATCH method
        elif self.request.method == 'PUT':
            return [IsMessageWriter()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        room_pk = self.kwargs.get('room_pk')
        if room_pk:
            return Message.objects.filter(room_id=room_pk).select_related('user').order_by('created')
        return Message.objects.all().select_related('user', 'room').order_by('-created')

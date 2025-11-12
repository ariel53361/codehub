from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from chat.filters import RoomFilter
from chat.permissions import IsMessageWriter, IsCurrentUser
from django.db.models.aggregates import Count, Max
from .models import Profile, Topic, Message, Room
from .serializers import CreateRoomSerializer, ProfileReadAndUpdateSerializer, TopicSerializer, MessageSerializer, RoomSerializer


class ProfileViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Profile.objects.all()
    http_method_names = ['get', 'patch', 'head', 'options']
    serializer_class = ProfileReadAndUpdateSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH']:
            return [IsCurrentUser()]
        return [AllowAny()]

    @action(detail=False, methods=['GET', 'PATCH'])
    def me(self, request):
        (proflie, created) = Profile.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = ProfileReadAndUpdateSerializer(proflie)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = ProfileReadAndUpdateSerializer(
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
            return {'user_id': self.request.user.id,
                    'topic_id': self.kwargs['topic_id']}
        return {'user_id': self.request.user.id}


class MessageViewSet(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,  mixins.CreateModelMixin, mixins.DestroyModelMixin):
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']
    serializer_class = MessageSerializer

    def get_serializer_context(self):
        room_pk = self.kwargs.get('room_pk')
        if room_pk:
            return {'user_id': self.request.user.id, 'room_id': self.kwargs['room_pk']}
        return {}

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        # for some reason the IsMessageWriter permission is not working with the PATCH method
        elif self.request.method == 'PUT':
            return [IsMessageWriter()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        room_pk = self.kwargs.get('room_pk')
        if room_pk:
            return Message.objects.filter(room_id=room_pk).select_related('user').order_by('-created')
        return Message.objects.all().select_related('user', 'room').order_by('-created')


# # This class extends Djoser's TokenCreateView to customize how tokens are created and returned
# class CustomTokenCreateView(TokenCreateView):
#     # This method is called after user credentials are validated
#     # It receives the serializer containing the authenticated user
#     def _action(self, serializer):
#         # Create both refresh and access tokens for the authenticated user
#         # token is the refresh token object, which also contains the access token
#         token = RefreshToken.for_user(serializer.user)

#         # Create the response object
#         # Only include access token in JSON body - frontend will store this
#         # The refresh token will be sent as a cookie instead
#         response = Response(
#             {
#                 'access': str(token.access_token),
#             },
#             status=status.HTTP_200_OK,
#         )

#         # Set the refresh token as a cookie
#         response.set_cookie(
#             key='refresh_token',      # Name of the cookie
#             value=str(token),         # The refresh token value
#             expires=None,             # Cookie expires when browser closes
#             secure=False,              # Cookie only sent over HTTPS
#             httponly=True,            # Cookie cannot be accessed by JavaScript
#             samesite='Lax'           # Protects against CSRF attacks
#         )

#         # Return the response with both:
#         # - access token in response body (for frontend to store)
#         # - refresh token in cookie (automatically handled by browser)
#         return response

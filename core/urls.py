from django.views.generic import TemplateView
from rest_framework_nested import routers
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('',TemplateView.as_view(template_name='codehub/index.html')),
    path('messages/', views.MessageViewSet.as_view(
        {'get': 'list'}), name='messages'),
    path('rooms/<int:room_pk>/messages/', views.MessageViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='room-messages'),
    path('rooms/<int:room_pk>/messages/<int:pk>/', views.MessageViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='room-message-detail'),
    # path('rooms/by-topic/<int:topic_id>/',
    #      views.RoomViewSet.as_view({'get': 'list', 'post': 'create'}), name='rooms-by-topic'),
    path('rooms/<int:pk>/', views.RoomViewSet.as_view(
         {'get': 'retrieve', 'delete': 'destroy'}), name='room-detail'),
    path('rooms/', views.RoomViewSet.as_view(
        {'get': 'list',  'delete': 'destroy', 'post': 'create'}), name='all-rooms'),
    path('topics/<int:pk>/', views.TopicViewSet.as_view(
        {'get': 'retrieve', 'post': 'create', 'delete': 'destroy'}), name='topic-detail'),
    path('topics/', views.TopicViewSet.as_view(
        {'get': 'list'}), name='all-topics'),
    path('users/<int:pk>', views.UserViewSet.as_view(
        {'get': 'retrieve', 'patch':'update'}), name='users'),
]


# router = routers.DefaultRouter()
# router.register('users', views.UserViewSet)
# router.register('topics', views.TopicViewSet)

# topics_router = routers.NestedDefaultRouter(
#     router, 'topics', lookup='topic')
# topics_router.register('rooms', views.RoomViewSet,
#                        basename='topic-rooms')

# urlpatterns = [
#     path('rooms/<int:room_pk>/messages/', views.MessageViewSet.as_view(
#         {'get': 'list', 'post': 'create'}), name='room-messages'),
#     path('rooms/<int:room_pk>/messages/<int:pk>/', views.MessageViewSet.as_view(
#         {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='room-message-detail'),
#     path('rooms/by-topic/<int:topic_id>/', views.RoomsByTopicView.as_view(), name='rooms-by-topic'),
#     path('rooms/', views.AllRoomsView.as_view(), name='all-rooms'),
# ] + router.urls + topics_router.urls

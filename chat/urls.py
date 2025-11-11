from django.urls import path
from rest_framework_nested import routers
from chat import views

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')

urlpatterns = [
    path('messages/', views.MessageViewSet.as_view(
        {'get': 'list'}), name='messages'),
    path('rooms/<int:room_pk>/messages/', views.MessageViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='room-messages'),
    path('rooms/<int:room_pk>/messages/<int:pk>/', views.MessageViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='room-message-detail'),
    path('rooms/<int:pk>/', views.RoomViewSet.as_view(
         {'get': 'retrieve', 'delete': 'destroy'}), name='room-detail'),
    path('rooms/', views.RoomViewSet.as_view(
        {'get': 'list',  'delete': 'destroy', 'post': 'create'}), name='all-rooms'),
    path('topics/<int:pk>/', views.TopicViewSet.as_view(
        {'get': 'retrieve', 'post': 'create', 'delete': 'destroy'}), name='topic-detail'),
    path('topics/', views.TopicViewSet.as_view(
        {'get': 'list'}), name='all-topics'),
] + router.urls

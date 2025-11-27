from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from . import views


router = DefaultRouter()
router.register('profiles', views.ProfileViewSet, basename='profiles')
router.register('rooms', views.RoomViewSet, basename='rooms')
router.register('topics', views.TopicViewSet, basename='topics')

rooms_router = NestedDefaultRouter(router, 'rooms', lookup='room')
rooms_router.register('messages', views.MessageViewSet, basename='room-messages')

urlpatterns = router.urls + rooms_router.urls

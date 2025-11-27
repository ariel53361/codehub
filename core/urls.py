from django.views.generic import TemplateView
from django.urls import path
from rest_framework.routers import DefaultRouter
from core.views import UserViewSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/index.html')),
    ] + router.urls

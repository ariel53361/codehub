from rest_framework import permissions
from chat.models import Message, Profile
from django.contrib.auth.models import AnonymousUser


class IsMessageWriter(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return not isinstance(request.user, AnonymousUser) and \
            Message.objects.filter(
                pk=view.kwargs['pk'], user=request.user).exists()


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

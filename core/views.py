from django.contrib.auth import get_user_model
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

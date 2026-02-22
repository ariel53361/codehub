from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.throttling import ScopedRateThrottle
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

User = get_user_model()


class CustomUserViewSet(DjoserUserViewSet):
    throttle_classes = [ScopedRateThrottle]

    def get_throttles(self):
        if self.action == "resend_activation":
            self.throttle_scope = "resend_activation"
            return super().get_throttles()

        if self.action == "reset_password":
            self.throttle_scope = "reset_password"
            return super().get_throttles()

        return []

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email__iexact=email).first()

        if user and user.is_active:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return super().resend_activation(request, *args, **kwargs)

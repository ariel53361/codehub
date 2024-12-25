from djoser.views import TokenCreateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .utils import set_jwt_cookie


class CookieTokenObtainView(TokenCreateView):
    def _action(self, serializer):
        token = RefreshToken.for_user(serializer.user)
        response = Response(
            {
                'access': str(token.access_token),
            },
            status=status.HTTP_200_OK,
        )
        set_jwt_cookie(response, str(token))
        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            set_jwt_cookie(response, request.data['refresh'])
            response.data = {
                'access': response.data['access']
            }

        return response

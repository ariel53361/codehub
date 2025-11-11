from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from chat.jwt_auth.auth_views import CookieTokenObtainView, CookieTokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

 

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('codehub/', include('chat.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/jwt/create/', CookieTokenObtainView.as_view(), name='jwt-create'),
    path('auth/jwt/refresh/', CookieTokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
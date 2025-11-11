from django.conf import settings


def set_jwt_cookie(response, token):
    response.set_cookie(
        settings.SIMPLE_JWT['AUTH_COOKIE'],
        token,
        max_age=settings.SIMPLE_JWT['AUTH_COOKIE_MAX_AGE'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
        path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']
    )

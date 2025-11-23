from django.conf import settings
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient
import pytest

from chat.models import Profile


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        user = baker.make(settings.AUTH_USER_MODEL, is_staff=is_staff)
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate

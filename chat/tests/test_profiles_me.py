from io import BytesIO
import os
from PIL import Image
from django.conf import settings
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from codehub.settings.common import MEDIA_URL


@pytest.fixture
def update_profile(api_client):
    def do_update_profile(**attributes):
        return api_client.patch('/codehub/profiles/me/', data=attributes)
    return do_update_profile


@pytest.fixture
def get_profile(api_client):
    def do_get_profile():
        return api_client.get('/codehub/profiles/me/')
    return do_get_profile


def generate_test_image_file(name="new_avatar.jpg"):
    file_obj = BytesIO()
    image = Image.new("RGB", (10, 10), "white")
    image.save(file_obj, format="JPEG")
    file_obj.seek(0)
    return SimpleUploadedFile(
        name=name,
        content=file_obj.getvalue(),
        content_type="image/jpeg"
    )


@pytest.mark.django_db
class TestUpdateProfile:
    def test_if_data_is_valid_return_200(self, authenticate, update_profile):
        user = authenticate(is_staff=False)
        profile = user.profile
        image_file = generate_test_image_file()
        bio = 'a'

        response = update_profile(bio=bio, avatar=image_file)
        profile.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert profile.user_id == user.id and \
            response.data['id'] == profile.id and \
            response.data['bio'] == bio and \
            response.data['avatar'] == profile.avatar.url and \
            response.data['user']['id'] == user.id

    def test_if_data_is_invalid_return_400(self, authenticate, update_profile):
        authenticate(is_staff=False)

        response = update_profile(avatar='a')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert isinstance(response.data['avatar'], list)

    def test_if_user_is_annonymous_return_401(self, update_profile):
        response = update_profile(bio='a')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestRetriveProfile:
    def test_if_user_is_authenticated_return_200(self, authenticate, get_profile):
        user = authenticate(is_staff=False)

        response = get_profile()

        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['id'] == user.id

    def test_if_user_is_annonymous_return_401(self, get_profile):
        response = get_profile()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

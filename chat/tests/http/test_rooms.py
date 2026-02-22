import pytest
from django.conf import settings
from model_bakery import baker
from rest_framework import status
from chat.models import Room, Topic


@pytest.mark.django_db
class TestRoomsList:
    def test_if_user_is_anonymous_return_200(self, api_client):
        quantity = 5
        users = baker.make(settings.AUTH_USER_MODEL, _quantity=quantity)
        for user in users:
            baker.make(Room, host=user.profile)
        response = api_client.get('/codehub/rooms/')
        results = response.data.get('results', response.data)

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == quantity


@pytest.mark.django_db
class TestRetrieveRoom:
    def test_if_user_is_anonymous_return_200(self, api_client):
        user = baker.make(settings.AUTH_USER_MODEL)
        room = baker.make(Room, host=user.profile)

        response = api_client.get(f'/codehub/rooms/{room.id}/')
        data = response.data

        assert response.status_code == status.HTTP_200_OK
        assert data['id'] == room.id
        assert data['host']['id'] == room.host.id
        assert data['topic']['id'] == room.topic.id

    def test_if_room_does_not_exists_return_404(self, api_client):
        response = api_client.get(f'/codehub/rooms/{1}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateRoom:
    def test_if_data_is_valid_return_201(self, api_client, authenticate):
        authenticate(is_staff=False)
        topic = baker.make(Topic)
        room = {
            'topic': topic.id,
            'subject': 'aa',
        }

        response = api_client.post(f'/codehub/rooms/', room)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['subject'] == room['subject']

    def test_if_data_is_invalid_return_400(self, api_client, authenticate):
        authenticate(is_staff=False)
        room = {
            'topic': 1,
            'subject': '',
        }

        response = api_client.post(f'/codehub/rooms/', room)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['topic'] is not None
        assert response.data['subject'] is not None

    def test_if_user_is_anonymous_return_401(self, api_client):
        topic = baker.make(Topic)
        room = {
            'topic': topic.id,
            'subject': 'aa',
        }

        response = api_client.post(f'/codehub/rooms/', room)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

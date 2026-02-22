from django.conf import settings
import pytest
from model_bakery import baker
from rest_framework import status
from chat.models import Message, Profile, Room


# @pytest.mark.django_db
# class TestCreateMessage:
#     def test_if_data_is_valid_return_201(self, api_client, authenticate):
#         user = authenticate(is_staff=False)
#         room = baker.make(Room, host=user.profile)
#         message = {'content': 'aa'}
#         print("room id: ", room.id)
#         response = api_client.post(
#             f'/codehub/rooms/{room.id}/messages/', message)

#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data['content'] == message['content']

#     def test_if_data_is_invalid_return_400(self, api_client, authenticate):
#         user = authenticate(is_staff=False)
#         room = baker.make(Room, host=user.profile)
#         message = {'content': ''}

#         response = api_client.post(
#             f'/codehub/rooms/{room.id}/messages/', message)

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['content'] is not None

#     def test_if_user_is_anonymous_return_401(self, api_client):
#         user = baker.make(settings.AUTH_USER_MODEL)
#         profile = Profile.objects.get(user__id=user.id)
#         room = baker.make(Room, host=profile)

#         response = api_client.post(
#             f'/codehub/rooms/{room.id}/messages/', {'content': 'aa'})

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert Message.objects.count() == 0

#     def test_if_room_does_not_exist_return_404(self, api_client, authenticate):
#         authenticate(is_staff=False)

#         response = api_client.post(
#             f'/codehub/rooms/{1}/messages/', {'content': 'aa'})

#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert Message.objects.count() == 0

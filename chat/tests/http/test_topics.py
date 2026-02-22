import pytest
from rest_framework.test import APIClient
from rest_framework import status
from chat.models import Topic


@pytest.mark.django_db
class TestTopicsList:
    def test_if_user_is_anonymous_return_200(self):
        Topic.objects.create(name="a")
        Topic.objects.create(name="b")
        client = APIClient()
        
        response = client.get('/codehub/topics/')
        results = response.data.get('results', response.data)

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 2


@pytest.mark.django_db
class TestRetriveTopic:
    def test_if_user_is_anonymous_return_200(self):
        Topic.objects.create(name="a")
        Topic.objects.create(name="b")
        pk = Topic.objects.get(name="a").pk
        client = APIClient()

        response = client.get(f'/codehub/topics/{pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "a"

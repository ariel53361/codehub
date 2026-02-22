import pytest
from django.core import mail


@pytest.mark.django_db
def test_create_user_sends_activation_email(api_client):
    payload = {
        "username": "ariel",
        "email": "ariel53361@gmail.com",
        "password": "strongpassword123"
    }

    response = api_client.post("/auth/users/", payload)
    email = mail.outbox[0]
    print("SUBJECT:", email.subject)

    print("FROM:", email.from_email)
    print("TO:", email.to)

    print("TEXT BODY:")
    print(email.body)
    assert response.status_code == 201
    assert len(mail.outbox) == 1

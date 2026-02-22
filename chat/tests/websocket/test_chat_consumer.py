import pytest
from uuid import uuid4
from channels.db import database_sync_to_async
from model_bakery import baker
from django.conf import settings
from chat.consumers import ACK_TYPE, CHAT_MESSAGE_TYPE
from rest_framework_simplejwt.tokens import AccessToken
from chat.models import Room, Message


@pytest.fixture
def message_counter():
    @database_sync_to_async
    def count(room_id: int, client_id: str) -> int:
        return Message.objects.filter(
            room_id=room_id,
            client_id=client_id
        ).count()

    return count


@pytest.mark.django_db
@pytest.mark.asyncio
class TestSendChatMessage():
    async def test_duplicate_ws_message_saved_once(
            self,
            ws_communicator,
            message_counter):

        @database_sync_to_async
        def setup_room_and_token():
            user = baker.make(settings.AUTH_USER_MODEL)
            room = baker.make(Room, host=user.profile)
            token = str(AccessToken.for_user(user))
            return token, room

        token, room = await setup_room_and_token()

        communicator = await ws_communicator(room.id, token)

        client_id = str(uuid4())
        payload = {
            "type": CHAT_MESSAGE_TYPE,
            "message": {"content": "hello", "client_id": client_id},
        }

        await communicator.send_json_to(payload)
        await communicator.send_json_to(payload)

        messages = [
            await communicator.receive_json_from(),
            await communicator.receive_json_from(),
            await communicator.receive_json_from(),
        ]

        acks = [m for m in messages if m.get("type") == ACK_TYPE]
        broadcasts = [m for m in messages if m.get(
            "type") == CHAT_MESSAGE_TYPE]

        assert len(acks) == 2
        assert len(broadcasts) == 1
        assert all(a["message"]["client_id"] == client_id for a in acks)

        assert await message_counter(room.id, client_id) == 1

        await communicator.disconnect()

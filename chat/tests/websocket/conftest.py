import pytest
from codehub.asgi import application
from channels.testing import WebsocketCommunicator


@pytest.fixture
def ws_communicator():
    async def _ws_communicator(room_id: int, token: str):
        path = f"/ws/rooms/{room_id}/?token={token}"
        communicator = WebsocketCommunicator(application, path)
        connected, _ = await communicator.connect()
        assert connected
        return communicator
    return _ws_communicator

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
import json
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.db import close_old_connections
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import User, Message, Room
from .serializers import MessageSerializer


GENERAL_WS_ERROR = 4000
TOKEN_EXPIRED = 4001
TOKEN_MISSING = 4002
INVALID_MESSAGE_FORMAT = 4003

ERROR_TYPE = "ws_error"
CHAT_MESSAGE_TYPE = "chat_message"


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode()
        token = parse_qs(query_string).get('token', [None])[0]

        if not token:
            await self.close()
            return

        try:
            user = await self.authenticate_user(token)
            self.scope['access_token'] = token
            self.scope['user'] = user
        except InvalidToken as e:
            print("InvalidToken")
            await self.close()
            return
        except Exception as e:
            await self.close()
            return
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        room_exists = await self.room_exists(self.room_id)
        if not room_exists:
            await self.close()
            return

        self.room_group_name = f'chat_{self.room_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        try:
            token = self.scope.get('access_token')

            if not token:
                await self.send_to_client(ERROR_TYPE, TOKEN_MISSING, "Token is missing")
                await self.close(code=TOKEN_EXPIRED)

            self.scope['user'] = await self.authenticate_user(token)

            data = json.loads(text_data)

            if data.get("type") == "ping":
                await self.send_to_client("pong")
                print("sent pong")
                return

            else:
                if "message" not in data or "content" not in data["message"]:
                    await self.send_to_client(ERROR_TYPE, INVALID_MESSAGE_FORMAT, "Invalid message format: expected message.content")
                    self.close(code=INVALID_MESSAGE_FORMAT)
                    return

                message_content = data['message']['content']
                user_id = self.scope['user'].id
                user = await database_sync_to_async(User.objects.get)(pk=user_id)
                room = await database_sync_to_async(Room.objects.get)(pk=self.room_id)

                message = await database_sync_to_async(Message.objects.create)(
                    user=user, room=room, content=message_content
                )

                await self.add_participant_if_needed(room, user)

                message_data = await self.serialize_message(message)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': CHAT_MESSAGE_TYPE,
                        'message': message_data,
                    }
                )

        except InvalidToken as e:
            print(e)
            await self.send_to_client(ERROR_TYPE, TOKEN_EXPIRED, "Invalid or expired token")
            await self.close(code=TOKEN_EXPIRED)
            return
        except Exception as e:
            print("WebSocket receive error:", e)
            await self.send_to_client(ERROR_TYPE, GENERAL_WS_ERROR, "General error")
            await self.close(code=GENERAL_WS_ERROR)

    @database_sync_to_async
    def validate_token(self, token, jwt_auth):
        validated_token = jwt_auth.get_validated_token(token)
        return validated_token

    @database_sync_to_async
    def get_user_from_token(self, validated_token, jwt_auth):
        user = jwt_auth.get_user(validated_token)
        close_old_connections()
        return user

    async def authenticate_user(self, token):
        jwt_auth = JWTAuthentication()
        validated_token = await self.validate_token(token, jwt_auth)
        user = await self.get_user_from_token(validated_token, jwt_auth)
        return user

    @database_sync_to_async
    def room_exists(self, room_id):
        return Room.objects.filter(id=room_id).exists()

    async def chat_message(self, event):
        print("Sending to WebSocket:", event['message'])
        await self.send_to_client(message=event['message'])

# אפשר לוותר
    @database_sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data

# לוודא רק שלא מוסיף משתמש קיים וזהו
    @database_sync_to_async
    def add_participant_if_needed(self, room, user):
        if room.host.id != user.id:
            room.participants.add(user)

    async def send_to_client(self, type: str = CHAT_MESSAGE_TYPE, code: int = None, message: dict = None):
        payload = {k: v for k, v in (
            ("type", type), ("message", message), ("code", code)) if v is not None}
        print("Sending to WebSocket:", payload)
        await self.send(text_data=json.dumps(payload))

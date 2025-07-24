from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
import json
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.db import close_old_connections
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import User, Message, Room


GENERAL_WS_ERROR = 4000
TOKEN_EXPIRED = 4001
TOKEN_MISSING = 4002


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode()
        token = parse_qs(query_string).get('token', [None])[0]

        if not token:
            await self.close()
            return

        try:
            validated_token = await self.validate_token(token)
            print("validating token complited")
            user = await self.get_user_from_token(validated_token)
            print("getting user complited")
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
                await self.send(text_data=json.dumps({
                    "type": "ws_error",
                    "code": TOKEN_MISSING,
                    "message": "Token is missing"
                }))
                await self.close(code=TOKEN_EXPIRED)

            validated_token = await self.validate_token(token)
            user = await self.get_user_from_token(validated_token)
            self.scope['user'] = user

            data = json.loads(text_data)

            if data.get("type") == "ping":
                await self.send(text_data=json.dumps({"type": "pong"}))
                print("sent pong")
                return

            else:
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
                        'type': 'chat_message',
                        'message': message_data,
                    }
                )

        except InvalidToken as e:
            print(e)

            await self.send(text_data=json.dumps({
                "type": "ws_error",
                "code": TOKEN_EXPIRED,
                "message": "Invalid or expired token"
            }))
            await self.close(code=TOKEN_EXPIRED)
        except Exception as e:

            print("WebSocket receive error:", e)
            await self.send(text_data=json.dumps({
                "type": "ws_error",
                "code": GENERAL_WS_ERROR,
                "message": "General error"
            }))
            await self.close(code=GENERAL_WS_ERROR)

    @database_sync_to_async
    def validate_token(self, token):
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        return validated_token

    @database_sync_to_async
    def get_user_from_token(self, validated_token):
        jwt_auth = JWTAuthentication()
        user = jwt_auth.get_user(validated_token)
        close_old_connections()
        return user

    @database_sync_to_async
    def room_exists(self, room_id):

        return Room.objects.filter(id=room_id).exists()

    async def chat_message(self, event):
        print("Sending to WebSocket:", event['message'])
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
        }))

    @database_sync_to_async
    def serialize_message(self, message):
        from .serializers import MessageSerializer
        return MessageSerializer(message).data

    @database_sync_to_async
    def add_participant_if_needed(self, room, user):
        if room.host.id != user.id:
            room.participants.add(user)

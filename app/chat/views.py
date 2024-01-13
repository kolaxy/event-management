from rest_framework import generics, permissions
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

class ChatRoomDetailView(generics.RetrieveAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Try to get the chat room for the current user, create if not exists
        chat_room, created = ChatRoom.objects.get_or_create(members=self.request.user)

        # Fetch all messages related to the chat room
        messages = Message.objects.filter(room=chat_room)

        # Attach the messages to the chat room object
        chat_room.messages = messages

        return chat_room

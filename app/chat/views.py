from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer
from users.models import User


class ChatRoomDetailView(generics.RetrieveAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        reciever_id = self.kwargs.get("room_name")
        self.reciever = User.objects.get(id=reciever_id)

        chat_room = ChatRoom.objects.filter(
            members__in=[self.request.user, self.reciever]
        ).first()

        if not chat_room:
            chat_room = ChatRoom.objects.create()
            chat_room.members.add(self.request.user, self.reciever)

        return chat_room

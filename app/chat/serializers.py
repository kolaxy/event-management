from rest_framework import serializers
from .models import ChatRoom, Message



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['user', 'id', 'content', 'created_at', 'room']

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = ChatRoom
        fields = ['id', 'members', 'created_at', 'messages']
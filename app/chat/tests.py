from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ChatRoom, Message
from .serializers import MessageSerializer, ChatRoomSerializer


User = get_user_model()

class ChatRoomModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1', password='password1')
        self.user2 = User.objects.create_user(email='user2', password='password2')

    def test_create_chat_room(self):
        chat_room = ChatRoom.objects.create()
        chat_room.members.add(self.user1, self.user2)

        self.assertEqual(chat_room.members.count(), 2)
        self.assertIsNotNone(chat_room.created_at)

    def test_chat_room_str(self):
        chat_room = ChatRoom.objects.create()
        self.assertEqual(str(chat_room), str(chat_room.id))

class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser', password='testpassword')
        self.chat_room = ChatRoom.objects.create()
        self.message_content = 'Test message content'

    def test_create_message(self):
        message = Message.objects.create(
            user=self.user,
            room=self.chat_room,
            content=self.message_content
        )

        self.assertEqual(message.user, self.user)
        self.assertEqual(message.room, self.chat_room)
        self.assertEqual(message.content, self.message_content)
        self.assertIsNotNone(message.created_at)

    def test_message_str(self):
        message = Message.objects.create(
            user=self.user,
            room=self.chat_room,
            content=self.message_content
        )

        self.assertEqual(str(message), self.message_content)



class ChatRoomDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.recipient = User.objects.create_user(email='recipient@example.com', password='recipientpassword')

    def test_get_existing_chat_room(self):
        chat_room = ChatRoom.objects.create()
        chat_room.members.add(self.user, self.recipient)

        self.client.force_authenticate(user=self.user)

        url = reverse('chat-room-detail-or-create', kwargs={'room_name': str(self.recipient.id)})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(chat_room.id))

    def test_get_or_create_new_chat_room(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('chat-room-detail-or-create', kwargs={'room_name': str(self.recipient.id)})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['id'])

        new_chat_room = ChatRoom.objects.filter(members__in=[self.user, self.recipient]).first()

        self.assertIsNotNone(new_chat_room)
        self.assertEqual(str(new_chat_room.id), response.data['id'])


class ChatRoomMessageSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser', password='testpassword')
        self.chat_room = ChatRoom.objects.create()
        self.chat_room.members.set([self.user])
        self.message = Message.objects.create(user=self.user, content='Test message', room=self.chat_room)


    def test_message_serializer(self):
        serializer = MessageSerializer(instance=self.message)
        data = serializer.data
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['content'], 'Test message')
        self.assertEqual(str(data['room']), str(self.chat_room.id))

    def test_chat_room_serializer(self):
        serializer = ChatRoomSerializer(instance=self.chat_room)
        data = serializer.data
        self.assertEqual(data['id'], str(self.chat_room.id))
        self.assertEqual(data['members'], [self.user.id])
        self.assertEqual(data['messages'][0]['id'], str(self.message.id))
        self.assertEqual(str(data['messages'][0]['user']), str(self.user.id))
        self.assertEqual(data['messages'][0]['content'], 'Test message')
        self.assertEqual(str(data['messages'][0]['room']), str(self.chat_room.id))

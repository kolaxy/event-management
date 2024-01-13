from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL


def validate_max_members(value):
    """
    We can edit logic in case of creating group chats.
    This is simple solution
    """
    if value.count() != 2:
        raise ValidationError('Only 2 members are allowed to create')


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages', blank=True, null=True)
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages', blank=True, null=True)
    room = models.ForeignKey(
        "ChatRoom", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.content


class ChatRoom(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    members = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return str(self.id)

    def clean(self):
        if self.members.count() != 2:
            raise ValidationError('You must select exactly 2 members for a chat room.')
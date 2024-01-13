from django.contrib import admin
from chat.models import Message, ChatRoom

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', "show_members")

    def show_members(self, obj):
        output = ', '.join(f'{str(member)} == {str(member.id)}' for member in obj.members.all())
        return output
    
    show_members.short_description = 'Members of the chat room'
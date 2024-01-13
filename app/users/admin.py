from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from users.models import User

admin.site.site_header = 'event-management admin'

@admin.register(User)
class MainUserAdmin(UserAdmin):
    change_user_password_template = None
    list_display = ('email', 'phone_number', 'added_at',)
    list_filter = ('added_at',)
    search_fields = ('email',)
    ordering = ('-added_at',)
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = [
        ['User additional data' , {
            'fields': ['phone_number']
        }],
        ['Authorization', {
            'fields': ['is_superuser', 'groups', 'user_permissions']
        }],
        ['Authentication', {
            'fields': ['email', 'password']
        }]
    ]
    add_fieldsets = [
        ['Authorization', {
            'fields': ['is_superuser', 'groups', 'user_permissions']
        }],
        ['Authenticated', {
            'fields': ['email', 'password1', 'password2']
        }]
    ]

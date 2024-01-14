from django.utils.html import format_html
from django.contrib import admin
from event.models import Event, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display =  ("title", "members_count","founder", "description", "founder", "id")
    search_fields = ("title", "description")

    def members_count(self, obj):
        return obj.members.count() + 1
    
    members_count.short_description = "Members count include admin"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "date", "preview_image")
    search_fields = ("title", "description", "date")
    list_filter = ("date", "organizations")

    def preview_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="25" height="25" />')
        return "No image"

    preview_image.short_description = 'Image Preview'

    readonly_fields = ('display_image', 'preview_image')

    def display_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="200" height="200" />')
        return "No image"

    display_image.short_description = 'Image Display'

    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'date', 'organizations'),
        }),
        ('Image', {
            'fields': ('image', 'display_image'),
        }),
    )

from django.utils.html import format_html
from django.contrib import admin
from event.models import Event, Organization



@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "date", "preview_image")
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



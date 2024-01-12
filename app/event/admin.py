from django.utils.html import format_html
from django.contrib import admin
from event.models import Event, Organization



@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "display_image", "date")

    def display_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="25" height="25" />')

    display_image.short_description = 'Image'

    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="200" height="200" />')

    preview_image.short_description = 'Image Preview'

    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'date', 'organizations'),
        }),
        ('Image', {
            'fields': ('image', 'preview_image'),
        }),
    )
from django.contrib import admin
from .models import AIChatLog


@admin.register(AIChatLog)
class AIChatLogAdmin(admin.ModelAdmin):
    """Admin for viewing chat logs."""

    list_display = ['timestamp', 'session_id', 'language', 'short_message']
    list_filter = ['language', 'timestamp']
    readonly_fields = ['timestamp', 'session_id', 'language', 'user_message', 'ai_response']
    search_fields = ['user_message', 'ai_response']
    date_hierarchy = 'timestamp'

    fieldsets = [
        ('Chat Info', {
            'fields': ['session_id', 'timestamp', 'language']
        }),
        ('Messages', {
            'fields': ['user_message', 'ai_response']
        }),
    ]

    def short_message(self, obj):
        """Truncate message for list view."""
        return (obj.user_message[:50] + '...') if len(obj.user_message) > 50 else obj.user_message
    short_message.short_description = 'User Message'

    def has_add_permission(self, request):
        """Logs are created automatically, not manually."""
        return False

from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from .models import ChatSupport
from chats.models import Chat

class ChatSupportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'last_message', 'is_open', 'created_date')
    list_filter = ('is_open', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'last_message')
    ordering = ['-is_open', 'created_date']  # Open chats on top, sorted by creation date
    readonly_fields = ('employee', 'last_message', 'is_open', 'created_date')  # Make all fields read-only
    change_form_template = "admin/support/chat_support/change_form.html"  # Use a custom template

    def render_change_form(self, request, context, *args, **kwargs):
        obj = kwargs.get('obj')
        if obj:
            # Get all chat messages related to the employee of the current ChatSupport instance
            chats = Chat.objects.filter(employee=obj.employee)
            context['related_chats'] = chats
        return super().render_change_form(request, context, *args, **kwargs)

admin.site.register(ChatSupport, ChatSupportAdmin)

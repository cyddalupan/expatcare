from django.contrib import admin
from .models import ChatSupport

class ChatSupportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'last_message', 'is_open', 'created_date')
    list_filter = ('is_open', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name', 'last_message')
    ordering = ['-is_open', 'created_date']  # Open chats on top, sorted by creation date

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # If needed, filter to display only open chats
        return queryset

admin.site.register(ChatSupport, ChatSupportAdmin)

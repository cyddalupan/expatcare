from django.contrib import admin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('employee', 'agency', 'sender', 'timestamp', 'is_support')
    list_filter = ('agency', 'sender', 'is_support')
    search_fields = ('employee__first_name', 'employee__last_name', 'message')

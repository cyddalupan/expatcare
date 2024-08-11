from django.contrib import admin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('employee', 'timestamp')
    #list_filter = ('employee', 'agency', 'sender')
    #search_fields = ('employee__first_name', 'employee__last_name', 'agency__username', 'message')

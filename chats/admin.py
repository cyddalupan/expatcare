from django.contrib import admin
from employee.models import Employee
from .models import Chat

admin.site.unregister(Employee)

class ChatInline(admin.TabularInline):
    model = Chat
    fields = ('message', 'sender', 'timestamp')
    readonly_fields = ('message', 'sender', 'timestamp')
    extra = 0
    can_delete = False
    show_change_link = False

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'passport_number', 'agency')
    search_fields = ('first_name', 'last_name', 'passport_number', 'agency__username')
    inlines = [ChatInline]

from django.contrib import admin
from .models import AICategory

class AICategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'role', 'updated_at')

admin.site.register(AICategory, AICategoryAdmin)

from django.contrib import admin

from advance.forms import AICategoryForm
from .models import AICategory

class AICategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'role', 'updated_at')
    form = AICategoryForm

admin.site.register(AICategory, AICategoryAdmin)

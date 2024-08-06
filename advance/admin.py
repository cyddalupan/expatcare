from django.contrib import admin

from advance.forms import AICategoryForm
from .models import AICategory, Setting

class AICategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'role', 'updated_at')
    form = AICategoryForm

class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'value_type')
    search_fields = ('name',)
    list_filter = ('value_type',)

admin.site.register(AICategory, AICategoryAdmin)
admin.site.register(Setting, SettingAdmin)

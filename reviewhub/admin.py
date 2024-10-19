from django.contrib import admin
from .models import StatementOfFact

@admin.register(StatementOfFact)
class StatementOfFactAdmin(admin.ModelAdmin):
    list_display = ('title', 'employee', 'creator', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'employee')
    search_fields = ('title', 'content', 'employee__first_name', 'employee__last_name')
    autocomplete_fields = ['employee', 'creator']

    # Override save_model to set the creator automatically
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set creator on creation
            obj.creator = request.user
        super().save_model(request, obj, form, change)

from django.contrib import admin
from .models import StatementOfFacts

class StatementOfFactsAdmin(admin.ModelAdmin):
    list_display = ('employee', 'status', 'date_created', 'date_updated')
    search_fields = ('employee__name', 'case__category')

admin.site.register(StatementOfFacts, StatementOfFactsAdmin)

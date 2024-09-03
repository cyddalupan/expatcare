from django.contrib import admin
from .models import Case

class CaseAdmin(admin.ModelAdmin):
    list_display = ('category', 'employee', 'updated_date', 'report_status', 'agency')
    search_fields = ('category', 'employee__first_name', 'employee__last_name', 'report_status', 'agency__username')
    list_filter = ('report_status', 'updated_date', 'date_reported', 'agency')
    readonly_fields = ('updated_date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Agency').exists():
            return qs.filter(agency=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change or not obj.agency:
            obj.agency = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        # Get the form and remove the 'agency' field from the fields
        form = super().get_form(request, obj, **kwargs)
        if 'agency' in form.base_fields:
            del form.base_fields['agency']
        return form

admin.site.register(Case, CaseAdmin)

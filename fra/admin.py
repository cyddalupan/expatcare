from django.contrib import admin
from .models import FRA

@admin.register(FRA)
class FRAAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'country', 'agency')
    search_fields = ('name', 'contact', 'country')
    list_filter = ('country',)
    
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
        form = super().get_form(request, obj, **kwargs)
        if 'agency' in form.base_fields:
            del form.base_fields['agency']
        return form

    class Meta:
        verbose_name = "FRA's"
        verbose_name_plural = "FRA's"

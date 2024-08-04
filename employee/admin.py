from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 
        'middle_name', 
        'last_name', 
        'passport_number', 
        'date_of_birth', 
        'address', 
        'phone_number', 
        'email', 
        'agency', 
        'emergency_contact_name',
    )
    search_fields = (
        'first_name', 
        'middle_name', 
        'last_name', 
        'passport_number', 
        'phone_number', 
        'email',
        'agency__username', 
        'address', 
        'emergency_contact_name', 
    )
    list_filter = (
        'date_of_birth',
    )
    fieldsets = (
        (None, {
            'fields': (
                'first_name', 
                'middle_name', 
                'last_name', 
                'passport_number', 
                'date_of_birth', 
                'address', 
                'phone_number', 
                'email',
            )
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name', 
                'emergency_contact_phone'
            )
        }),
    )

    def agency_name(self, obj):
        return obj.agency.username 
    agency_name.admin_order_field = 'agency__username' 
    agency_name.short_description = 'Agency Username' 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Agency').exists():
            # Assuming that the 'agency' field is a ForeignKey to the User model
            return qs.filter(agency=request.user)
        return qs
    def save_model(self, request, obj, form, change):
        if not change or not obj.agency:
            # Only set the agency if the object is new or doesn't have one
            obj.agency = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Employee, EmployeeAdmin)

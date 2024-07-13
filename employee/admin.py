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
        'emergency_contact_name', 
        'emergency_contact_phone'
    )
    search_fields = (
        'first_name', 
        'last_name', 
        'passport_number', 
        'phone_number', 
        'email'
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
                'email'
            )
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name', 
                'emergency_contact_phone'
            )
        }),
    )

admin.site.register(Employee, EmployeeAdmin)

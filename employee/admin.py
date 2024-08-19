from django.contrib import admin
from .models import Employee
from cases.models import Case
from chats.models import Chat

class ChatInline(admin.TabularInline):
    model = Chat
    fields = ('sender', 'message', 'timestamp')
    readonly_fields = ('sender', 'message', 'timestamp')
    extra = 0
    can_delete = False
    show_change_link = False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-timestamp')

class CaseInline(admin.TabularInline):
    model = Case
    fields = ('category', 'date_reported', 'report_status', 'agency')
    readonly_fields = ('category', 'date_reported', 'report_status', 'agency')
    extra = 0
    can_delete = False
    show_change_link = False

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
        'date_deployment',
        'fra',
        'main_status',
        'applicant_type',
        'created_date_of_report',
        'country',
        'consistency_percentage',
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
        'fra__name',
        'main_status',
        'applicant_type',
        'country',
    )
    list_filter = (
        'date_of_birth',
        'date_deployment',
        'fra',
        'main_status',
        'applicant_type',
        'country',
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
                'date_deployment',
                'fra',
                'main_status',
                'applicant_type',
                'created_date_of_report',
                'country',
                'facebook',
                'whatsapp',
                'consistency_percentage',
            )
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name', 
                'emergency_contact_phone'
            )
        }),
    )

    inlines = [CaseInline, ChatInline]

    def agency_name(self, obj):
        return obj.agency.username 
    agency_name.admin_order_field = 'agency__username' 
    agency_name.short_description = 'Agency Username' 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Agency').exists():
            return qs.filter(agency=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change or not obj.agency:
            obj.agency = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Employee, EmployeeAdmin)

from django.contrib import admin
from django.http import HttpResponse
from dotenv import load_dotenv
from openai import OpenAI
from rangefilter.filters import DateRangeFilter
from django.urls import path
from django.utils.html import format_html
import pandas as pd
from django.urls import reverse
from .models import Employee
from cases.models import Case
from chats.models import Chat

load_dotenv()

client = OpenAI()

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
    fields = ('case_link', 'category', 'date_reported', 'report_status', 'agency')
    readonly_fields = ('case_link', 'category', 'date_reported', 'report_status', 'agency')
    extra = 0
    can_delete = False
    show_change_link = False

    def case_link(self, obj):
        link = reverse("admin:cases_case_change", args=[obj.id])  # admin:appname_modelname_change
        return format_html('<a href="{}">{}</a>', link, obj.category)
    case_link.short_description = 'Case'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-cases/', self.admin_site.admin_view(self.export_cases), name='export_cases'),
        ]
        return custom_urls + urls

    def export_cases(self, request):
        # Get the list of cases for the selected employee
        employee_id = request.GET.get('employee_id')
        if not employee_id:
            self.message_user(request, "No employee selected")
            return HttpResponse(status=400)
        
        cases = Case.objects.filter(employee_id=employee_id)
        data = []
        for case in cases:
            data.append({
                'Category': case.category,
                'Date Reported': case.date_reported,
                'Report Status': case.report_status,
                'Agency': case.agency.name if case.agency else None,
            })

        # Create a DataFrame and export to Excel
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="cases.xlsx"'
        df.to_excel(response, index=False)
        return response

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
        'export_cases_link', 
        'generate_statement_link',
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
        ('date_deployment', DateRangeFilter),
        'date_of_birth',
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

    def export_cases_link(self, obj):
        url = reverse("admin:export_cases") + f"?employee_id={obj.id}"
        return format_html('<a class="button" href="{}">Export Cases to Excel</a>', url)
    export_cases_link.short_description = "Export Cases"

    def generate_statement_link(self, obj):
        url = reverse("admin:generate_statement") + f"?employee_id={obj.id}"
        return format_html('<a class="button" href="{}">Generate Statement of Facts</a>', url)
    generate_statement_link.short_description = "Generate Statement of Facts"

    # Registering the custom export URL
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-cases/', self.admin_site.admin_view(self.export_cases), name='export_cases'),
            path('generate-statement/', self.admin_site.admin_view(self.generate_statement), name='generate_statement'),
        ]
        return custom_urls + urls

    def export_cases(self, request):
        employee_id = request.GET.get('employee_id')
        if not employee_id:
            self.message_user(request, "No employee selected")
            return HttpResponse(status=400)
        
        # Fetching the cases related to the selected employee
        cases = Case.objects.filter(employee_id=employee_id)
        data = []
        for case in cases:
            data.append({
                'Category': case.category,
                'Date Reported': case.date_reported.replace(tzinfo=None) if case.date_reported else None,
                'Report Status': case.report_status,
                'Agency': case.agency.username if case.agency else None,
                'Report Details': case.report,
            })

        # Creating a DataFrame and exporting to Excel
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="cases.xlsx"'
        df.to_excel(response, index=False)
        return response

    def generate_statement(self, request):
        # This will handle the statement generation logic.
        # For now, it can just return a simple response to indicate the button works.
        return HttpResponse("Generate Statement of Facts button clicked!")

admin.site.register(Employee, EmployeeAdmin)

def create_statement(article):
    messages = [
        {"role": "system", "content": 'You are an AI model tasked with generating a "Statement of Facts" for a case involving an employee, with the goal of favoring the agency while still maintaining a fair, win-win tone where possible. The "Statement of Facts" should be clear, concise, and factual, summarizing the key details and events relevant to the case.'},
    ]

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return None
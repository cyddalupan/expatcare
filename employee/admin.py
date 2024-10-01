# Standard library imports
import pandas as pd

# Third-party imports
from dotenv import load_dotenv
from openai import OpenAI
from django.contrib import admin, messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.contrib.admin import DateFieldListFilter

# Local app imports
from .models import Employee, EmployeeMemory, EmployeeArrived, EmployeeBlacklisted, EmployeeClosedCases, EmployeeNoCommunication, EmployeeWithComplaints, EmployeeWithHearings
from .forms import EmotionSelectionForm
from cases.models import Case
from chats.models import Chat
from statement_of_facts.models import StatementOfFacts
from .utils import create_statement, build_consistency_analysis

load_dotenv()

client = OpenAI()

class BaseInline(admin.TabularInline):
    extra = 0
    can_delete = False
    show_change_link = False
    ordering_field = 'timestamp'

    readonly_fields = ('timestamp',)

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by(f'-{self.ordering_field}')

class ChatInline(BaseInline):
    model = Chat
    fields = ('sender', 'message', 'timestamp')
    readonly_fields = ('sender', 'message', 'timestamp')

    ordering_field = 'timestamp'

class CaseInline(BaseInline):
    model = Case
    fields = ('case_link', 'category', 'updated_date', 'report_status', 'agency')
    readonly_fields = ('case_link', 'category', 'updated_date', 'report_status', 'agency')

    ordering_field = 'date_reported'

    def case_link(self, obj):
        link = reverse("admin:cases_case_change", args=[obj.id])  # admin:appname_modelname_change
        return format_html('<a href="{}">{}</a>', link, obj.category)
    case_link.short_description = 'Case'


class StatementOfFactsInline(BaseInline):
    model = StatementOfFacts
    verbose_name_plural = "Statements of Facts"
    extra = 0
    readonly_fields = ('formatted_text', 'formatted_analysis', 'date_created', 'date_updated')
    fields = ('formatted_text', 'formatted_analysis', 'ai_reference_link', 'status', 'emotion', 'date_created')
    ordering_field = 'date_created'

    def formatted_text(self, obj):
        return obj.formatted_text()

    def formatted_analysis(self, obj):
        return obj.formatted_analysis()

class EmployeeMemoryInline(admin.TabularInline):
    model = EmployeeMemory
    extra = 1
    fields = ('note', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)  # Order memories by the most recent first

    def has_add_permission(self, request, obj):
        # Only allow adding memories when viewing an employee
        return True if obj else False

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
        ('date_deployment', DateFieldListFilter),
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
    inlines = [CaseInline, ChatInline, StatementOfFactsInline, EmployeeMemoryInline]

    def agency_name(self, obj):
        return obj.agency.username 
    agency_name.admin_order_field = 'agency__username' 
    agency_name.short_description = 'Agency Username' 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(agency=request.user) if request.user.groups.filter(name='Agency').exists() else qs


    def save_model(self, request, obj, form, change):
        obj.agency = obj.agency or request.user
        super().save_model(request, obj, form, change)


    def export_cases_link(self, obj):
        url = f"{reverse('admin:export_cases')}?employee_id={obj.id}"
        return format_html('<a class="button" href="{}">Export Cases to Excel</a>', url)
    export_cases_link.short_description = "Export Cases"

    def generate_statement_link(self, obj):
        return format_html('<a href="{}">Generate Statement of Facts</a>', reverse('admin:employee-generate-statement', args=[obj.pk]))
    generate_statement_link.short_description = "Generate Statement of Facts"

    # Registering the custom export URL
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-cases/', self.admin_site.admin_view(self.export_cases), name='export_cases'),
            path('generate-statement/<int:employee_id>/', self.admin_site.admin_view(self.generate_statement), name='employee-generate-statement'),
            path('with-complaints/', self.admin_site.admin_view(self.with_complaints_view), name='employee-with-complaints'),
        ]
        return custom_urls + urls
    
    def with_complaints_view(self, request):
        employees = Employee.objects.filter(main_status='with_complain')
        context = dict(
            self.admin_site.each_context(request),
            title="Employees with Complaints",
            employees=employees,
        )
        return render(request, 'admin/employee/with_complaints.html', context)

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

    def generate_statement(self, request, employee_id):
        if 'apply' in request.POST:
            form = EmotionSelectionForm(request.POST)
            if form.is_valid():
                emotion = form.cleaned_data['emotion']
                include_consistency = form.cleaned_data.get('include_consistency_analysis', False)
                reference_link = form.cleaned_data.get('reference_link', "")
            
                consistency_analysis = ""

                if include_consistency:
                    # Fetch the last 25 chat messages for the employee
                    chat_history = Chat.objects.filter(employee_id=employee_id).order_by('-timestamp')[:30]
                    
                    # Convert chat history to a list of strings or however you need it for the analysis
                    chat_history = [f"{chat.sender}: {chat.message}" for chat in chat_history]
                    
                    # Perform the consistency analysis
                    consistency_analysis = build_consistency_analysis(chat_history)
                    
                generated_text = create_statement(employee_id, emotion, consistency_analysis, reference_link)

                employee = Employee.objects.get(id=employee_id)

                StatementOfFacts.objects.create(
                    employee=employee,
                    generated_text=generated_text,
                    emotion=emotion,
                    consistency_analysis_included=include_consistency,
                    consistency_analysis=consistency_analysis,
                    ai_reference_link=reference_link,
                    status='draft',
                )

                messages.success(request, 'Statement of Facts generated successfully.')
                return redirect(f'/admin/employee/employee/{employee_id}/change/#statement-of-factss-tab')
        else:
            form = EmotionSelectionForm()

        context = self.admin_site.each_context(request)
        context.update({
            'form': form,
            'employee_id': employee_id,
            'title': 'Select Emotion for Statement of Facts',
        })

        return TemplateResponse(request, "admin/emotion_selection_form.html", context)

admin.site.register(Employee, EmployeeAdmin)
class EmployeeWithComplaintsAdmin(EmployeeAdmin):
    list_filter = (
        ('date_deployment', DateFieldListFilter),
        'date_of_birth',
        'fra',
        'applicant_type',
        'country',
    )

    def get_queryset(self, request):
        # Filter employees to only show those with complaints
        queryset = super().get_queryset(request)
        return queryset.filter(main_status='with_complain')

    # Ensure a unique verbose name and plural name
    verbose_name = "Employee with Complaint"
    verbose_name_plural = "Employees with Complaints"

admin.site.register(EmployeeWithComplaints, EmployeeWithComplaintsAdmin)


class EmployeeWithHearingsAdmin(EmployeeAdmin):
    list_filter = (
        ('date_deployment', DateFieldListFilter),
        'date_of_birth',
        'fra',
        'applicant_type',
        'country',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(main_status='with_hearing')

    # Ensure a unique verbose name and plural name
    verbose_name = "Employee with Hearing"
    verbose_name_plural = "Employees with Hearings"

admin.site.register(EmployeeWithHearings, EmployeeWithHearingsAdmin)


class EmployeeNoCommunicationAdmin(EmployeeAdmin):
    list_filter = (
        ('date_deployment', DateFieldListFilter),
        'date_of_birth',
        'fra',
        'applicant_type',
        'country',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(main_status='no_communication').exclude(main_status='arrive')

    # Ensure a unique verbose name and plural name
    verbose_name = "Employee with No Communication"
    verbose_name_plural = "Employees with No Communication"

admin.site.register(EmployeeNoCommunication, EmployeeNoCommunicationAdmin)


class EmployeeClosedCasesAdmin(EmployeeAdmin):
    list_filter = (
        ('date_deployment', DateFieldListFilter),
        'date_of_birth',
        'fra',
        'applicant_type',
        'country',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(main_status='closed')

    # Ensure a unique verbose name and plural name
    verbose_name = "Employee with Closed Case"
    verbose_name_plural = "Employees with Closed Cases"

admin.site.register(EmployeeClosedCases, EmployeeClosedCasesAdmin)


class EmployeeArrivedAdmin(EmployeeAdmin):
    list_filter = (
        ('date_deployment', DateFieldListFilter),
        'date_of_birth',
        'fra',
        'applicant_type',
        'country',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(main_status='arrive')

    # Ensure a unique verbose name and plural name
    verbose_name = "Employee Arrived"
    verbose_name_plural = "Employees Arrived"

admin.site.register(EmployeeArrived, EmployeeArrivedAdmin)


class EmployeeBlacklistedAdmin(EmployeeAdmin):
    list_filter = (
        ('date_deployment', DateFieldListFilter),
        'date_of_birth',
        'fra',
        'applicant_type',
        'country',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(main_status='blacklist')

    # Ensure a unique verbose name and plural name
    verbose_name = "Blacklisted Employee"
    verbose_name_plural = "Blacklisted Employees"

admin.site.register(EmployeeBlacklisted, EmployeeBlacklistedAdmin)

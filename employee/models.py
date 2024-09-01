from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField  # Import CountryField from django-countries
from fra.models import FRA

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    
    date_deployment = models.DateField(null=True, blank=True)  # Date Deployment
    fra = models.ForeignKey(FRA, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign Recruitment Agency
    main_status = models.CharField(
        max_length=50, 
        choices=[
            ('active', 'Active'),
            ('with_complain', 'With Complain'),
            ('arrive', 'Arrive'),
            ('no_communication', 'No Communication'),
            ('with_hearing', 'With Hearing'),
            ('blacklist', 'Blacklist'),
        ],
        default='active'
    )
    
    applicant_type = models.CharField(
        max_length=50, 
        choices=[
            ('household', 'Household'),
            ('skilled', 'Skilled'),
        ],
        default='household'
    ) 
    
    created_date_of_report = models.DateField(null=True, blank=True)  # Created Date of Report
    country = CountryField()  # Country
    facebook = models.URLField(max_length=255, blank=True, null=True)  # Facebook
    whatsapp = models.CharField(max_length=20, blank=True, null=True)  # WhatsApp
    consistency_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Consistency Percentage
    
    agency = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Agency'}, related_name='employees')

    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"

class EmployeeWithComplaints(Employee):
    class Meta:
        proxy = True
        verbose_name = "Employee with Complaint"
        verbose_name_plural = "Employees with Complaints"

class EmployeeWithHearings(Employee):
    class Meta:
        proxy = True
        verbose_name = "Employee with Hearing"
        verbose_name_plural = "Employees with Hearings"

class EmployeeNoCommunication(Employee):
    class Meta:
        proxy = True
        verbose_name = "Employee with No Communication"
        verbose_name_plural = "Employees with No Communication"

class EmployeeClosedCases(Employee):
    class Meta:
        proxy = True
        verbose_name = "Employee with Closed Case"
        verbose_name_plural = "Employees with Closed Cases"

class EmployeeArrived(Employee):
    class Meta:
        proxy = True
        verbose_name = "Employee Arrived"
        verbose_name_plural = "Employees Arrived"

class EmployeeBlacklisted(Employee):
    class Meta:
        proxy = True
        verbose_name = "Blacklisted Employee"
        verbose_name_plural = "Blacklisted Employees"

from django.db import models
from django.contrib.auth.models import User
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
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    fra = models.ForeignKey(FRA, on_delete=models.SET_NULL, null=True, blank=True)
    agency = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Agency'}, related_name='employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"

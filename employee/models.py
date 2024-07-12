from django.db import models

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

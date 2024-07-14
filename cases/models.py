from django.db import models
from employee.models import Employee  # Import the Employee model

class Case(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='cases')
    category = models.CharField(max_length=50)
    summary = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.employee.first_name} {self.employee.last_name}"

from django.db import models
from employee.models import Employee  # Adjust the import based on your project structure

class StatementOfFacts(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='statements_of_facts')
    generated_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=[('draft', 'Draft'), ('finalized', 'Finalized')])

    def __str__(self):
        return f"Statement for {self.employee.name} - {self.date_created}"

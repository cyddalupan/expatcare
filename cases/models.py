# models.py

from django.db import models
from django.contrib.auth.models import User
from employee.models import Employee
from django.utils import timezone

class Case(models.Model):
    OPEN = 'open'
    INVESTIGATION = 'investigation'
    CLOSED = 'closed'
    PENDING = 'pending'
    REOPENED = 'reopened'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (INVESTIGATION, 'Investigation'),
        (CLOSED, 'Closed'),
        (PENDING, 'Pending'),
        (REOPENED, 'Reopened'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='cases')
    category = models.CharField(max_length=50)
    report = models.TextField() 
    date_reported = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)  # Automatically updates on save
    report_status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=OPEN,
    )
    agency = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')

    def __str__(self):
        return f"{self.category} - {self.employee.first_name} {self.employee.last_name} ({self.get_report_status_display()})"

class CaseComment(models.Model):
    case = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.case.category}"
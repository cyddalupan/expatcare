from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from employee.models import Employee

class Chat(models.Model):
    SENDER_CHOICES = [
        ('Employee', 'Employee'),
        ('AI', 'AI'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='chats')
    agency = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    message = models.TextField()
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    is_support = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.employee} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Chat"
        verbose_name_plural = "Chats"

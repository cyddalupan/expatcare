from django.db import models
from employee.models import Employee  # Import Employee model

class ChatSupport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='chats')
    last_message = models.TextField()
    is_open = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat with {self.employee.first_name} {self.employee.last_name} - {'Open' if self.is_open else 'Closed'}"

from django.db import models

class Task(models.Model):
    description = models.CharField(max_length=255)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.description

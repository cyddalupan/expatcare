from django.db import models

class Agency(models.Model):
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

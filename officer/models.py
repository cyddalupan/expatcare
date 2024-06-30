from django.db import models
from users.models import User
from agency.models import Agency

class OfficerInCharge(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

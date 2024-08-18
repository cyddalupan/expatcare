from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User

class FRA(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    address = models.TextField()
    country = CountryField()
    agency = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fras')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "FRA's"
        verbose_name_plural = "FRA's"

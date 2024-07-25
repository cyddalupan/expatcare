from django.db import models

class AICategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=500)
    function_description = models.CharField(max_length=500)
    param_one_name = models.CharField(max_length=100, blank=True, null=True)
    param_one_desc = models.CharField(max_length=255, blank=True, null=True)
    param_one_enum = models.CharField(max_length=255, blank=True, null=True)
    param_two_name = models.CharField(max_length=100, blank=True, null=True)
    param_two_desc = models.CharField(max_length=255, blank=True, null=True)
    param_two_enum = models.CharField(max_length=255, blank=True, null=True)
    param_three_name = models.CharField(max_length=100, blank=True, null=True)
    param_three_desc = models.CharField(max_length=255, blank=True, null=True)
    param_three_enum = models.CharField(max_length=255, blank=True, null=True)
    param_four_name = models.CharField(max_length=100, blank=True, null=True)
    param_four_desc = models.CharField(max_length=255, blank=True, null=True)
    param_four_enum = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name

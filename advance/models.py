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

class Setting(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    value_type = models.CharField(
        max_length=50,
        choices=[
            ('str', 'String'),
            ('int', 'Integer'),
            ('bool', 'Boolean'),
            ('float', 'Float'),
            ('json', 'JSON'),
        ],
        default='str'
    )

    def __str__(self):
        return f"{self.name}: {self.value}"

    def get_value(self):
        if self.value_type == 'int':
            return int(self.value)
        elif self.value_type == 'bool':
            return self.value.lower() in ('true', '1')
        elif self.value_type == 'float':
            return float(self.value)
        elif self.value_type == 'json':
            import json
            return json.loads(self.value)
        return self.value

    def set_value(self, new_value):
        if self.value_type == 'json':
            import json
            self.value = json.dumps(new_value)
        else:
            self.value = str(new_value)
        self.save()

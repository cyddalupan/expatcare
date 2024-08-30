from django.db import models
from employee.models import Employee  # Adjust the import based on your project structure
import markdown
from django.utils.safestring import mark_safe

class StatementOfFacts(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='statements_of_facts')
    generated_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=[('draft', 'Draft'), ('finalized', 'Finalized')])

    def __str__(self):
        return f"Statement for {self.employee.name} - {self.date_created}"

    def formatted_text(self):
        """Converts the markdown text to HTML and returns it as a safe string."""
        html = markdown.markdown(self.generated_text)
        return mark_safe(html)
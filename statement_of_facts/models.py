from django.db import models
from employee.models import Employee  # Adjust the import based on your project structure
import markdown
from django.utils.safestring import mark_safe

class StatementOfFacts(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='statements_of_facts')
    generated_text = models.TextField()
    emotion = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=[('draft', 'Draft'), ('finalized', 'Finalized')])
    consistency_analysis_included = models.BooleanField(default=False, help_text="Indicates whether consistency analysis was included in the statement.")
    consistency_analysis = models.TextField()
    ai_reference_link = models.URLField(max_length=200, blank=True, help_text="A URL for referencing this statement of facts.")

    def __str__(self):
        return f"Statement for {self.employee.name} - {self.date_created}"

    def formatted_text(self):
        """Converts the markdown text to HTML and returns it as a safe string."""
        html = markdown.markdown(self.generated_text)
        return mark_safe(html)
    
    def formatted_analysis(self):
        html = markdown.markdown(self.consistency_analysis)
        return mark_safe(html)
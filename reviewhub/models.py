from django.db import models
from django.contrib.auth.models import User  # For creator reference
from employee.models import Employee  # For employee involved

class StatementOfFact(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Employee involved
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='statements'
    )

    # Automatically set creator on save (read-only via frontend)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_statements',
        editable=False  # Prevent editing from forms
    )

    # Status with expanded workflow options
    status = models.CharField(
        max_length=50,
        choices=[
            ('new', 'New'),
            ('draft', 'Draft'),
            ('in_review', 'In Review'),
            ('approved', 'Approved'),
            ('submitted', 'Submitted'),
            ('rejected', 'Rejected'),
            ('revised', 'Revised'),
            ('finalized', 'Finalized'),
            ('archived', 'Archived')
        ],
        default='new'
    )

    # Read-only fields updated by backend logic
    score = models.PositiveIntegerField(
        blank=True, null=True,
        help_text="Score between 1 and 100."
    )
    suggestion = models.TextField(
        blank=True, null=True,
        help_text="Suggestions for improvement."
    )

    def __str__(self):
        return f"{self.title} - {self.employee.first_name} {self.employee.last_name}"

    def save(self, *args, **kwargs):
        # Ensure 'creator' is assigned only on creation
        if not self.pk and not self.creator_id:
            self.creator = kwargs.pop('user', None)

        super().save(*args, **kwargs)

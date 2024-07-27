# forms.py
from django import forms
from .models import AICategory

class AICategoryForm(forms.ModelForm):
    class Meta:
        model = AICategory
        fields = '__all__'
        widgets = {
            'role': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'function_description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'param_one_desc': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'param_two_desc': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'param_three_desc': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'param_four_desc': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

# forms.py in your employee app or statement_of_facts app
from django import forms

class EmotionSelectionForm(forms.Form):
    EMOTION_CHOICES = [
        ('neutral', 'Neutral'),
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        # Add more emotions as needed
    ]
    emotion = forms.ChoiceField(choices=EMOTION_CHOICES, label="Select Emotion")

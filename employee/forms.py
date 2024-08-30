# forms.py in your employee app or statement_of_facts app
from django import forms

class EmotionSelectionForm(forms.Form):
    EMOTION_CHOICES = [
        ('neutral', 'Neutral'),
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('apologetic', 'Apologetic'),
    ]
    emotion = forms.ChoiceField(choices=EMOTION_CHOICES, label="Select Emotion")
    include_consistency_analysis = forms.BooleanField(
        required=False,
        label="Include Consistency Analysis",
        help_text="If selected, the Statement of Facts will include an analysis of the applicant's chat history, "
                  "reviewing the consistency of their statements and adjusting the final summary based on the analysis."
    )
    reference_link = forms.TextInput()

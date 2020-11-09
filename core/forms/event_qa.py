from django import forms
from core.models import EventPracticeAudienceQA

# -----------------------------------------------------------------------------
# EventPracticeAudienceQA
# -----------------------------------------------------------------------------

class EventPracticeAudienceQAForm(forms.ModelForm):

    """Custom Banner Form"""

    class Meta():
        model = EventPracticeAudienceQA
        fields = [
            "event",
            'question',
            "answer",
            ]


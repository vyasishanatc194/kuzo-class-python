from django import forms
from core.models import Faq

# -----------------------------------------------------------------------------
# Faq
# -----------------------------------------------------------------------------

class FaqForm(forms.ModelForm):

    """Custom Banner Form"""

    class Meta():
        model = Faq
        fields = [
            "faq_types",
            'question',
            "answer",
            ]


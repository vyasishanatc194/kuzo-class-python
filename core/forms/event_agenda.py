from django import forms
from core.models import Agenda

# -----------------------------------------------------------------------------
# Agenda
# -----------------------------------------------------------------------------

class AgendaForm(forms.ModelForm):

    """Custom Agenda Form"""

    class Meta():
        model = Agenda
        fields = [
            "event",
            'title',
            "description",
            ]


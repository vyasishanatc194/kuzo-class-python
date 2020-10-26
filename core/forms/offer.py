from django import forms
from core.models import Offer

# -----------------------------------------------------------------------------
# Offer
# -----------------------------------------------------------------------------


class OfferForm(forms.ModelForm):

    """Custom Offer Form"""

    class Meta():
        model = Offer
        fields = [
            "title",
            "icon",
            "description",
            ]

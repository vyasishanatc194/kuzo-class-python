from django import forms
from core.models import Credit

# -----------------------------------------------------------------------------
# Credit
# -----------------------------------------------------------------------------


class CreditForm(forms.ModelForm):

    """ Custom Credit Form"""

    class Meta():
        model = Credit
        fields = [
            "price",
            "number_of_credit",
            ]
  
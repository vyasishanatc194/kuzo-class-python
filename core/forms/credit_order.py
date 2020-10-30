from django import forms
from core.models import CreditOrder

# -----------------------------------------------------------------------------
# CreditOrder
# -----------------------------------------------------------------------------


class CreditOrderForm(forms.ModelForm):

    """ Custom Credit Form"""

    class Meta():
        model = Credit
        fields = [
            "price",
            "number_of_credit",
            ]
  

  
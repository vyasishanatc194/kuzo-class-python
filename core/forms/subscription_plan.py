from django import forms
from core.models import SubscriptionPlan

# -----------------------------------------------------------------------------
# SubscriptionPlan
# -----------------------------------------------------------------------------


class SubscriptionPlanForm(forms.ModelForm):

    """Custom SubscriptionPlan Form"""

    class Meta():
        model = SubscriptionPlan
        fields = [
            "title",
            "price",
            "number_of_credit",
            "description",
            'stripe_plan_id',
            ]

       

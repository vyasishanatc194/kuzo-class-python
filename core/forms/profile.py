from django import forms
from core.models import UserProfile

# -----------------------------------------------------------------------------
# Credit
# -----------------------------------------------------------------------------


class UserProfileForm(forms.ModelForm):

    """ Custom Credit Form"""

    class Meta():
        model = UserProfile
        fields = ["user","influencer", "follower", "is_popular", ]


 
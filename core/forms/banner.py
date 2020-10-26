from django import forms
from core.models import Banner

# -----------------------------------------------------------------------------
# Banner
# -----------------------------------------------------------------------------


class BannerForm(forms.ModelForm):

    """Custom Banner Form"""

    class Meta():
        model = Banner
        fields = [
            "title",
            "image",
            "description",
            ]

from django import forms
from core.models import Category

# -----------------------------------------------------------------------------
# Category
# -----------------------------------------------------------------------------


class CategoryForm(forms.ModelForm):

    """Custom Category Form"""

    class Meta():
        model = Category
        fields = [
            "name",
            ]

# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission

# -----------------------------------------------------------------------------
# Util methods
# -----------------------------------------------------------------------------


def filter_perms():
    """Remove permissions we don't need to worry about managing."""
    return Permission.objects.exclude(
        content_type_id__app_label__in=settings.ADMIN_HIDE_PERMS
    )
 

# -----------------------------------------------------------------------------
# Groups
# -----------------------------------------------------------------------------


class MyGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "permissions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # filter out the permissions we don't want the user to see
        self.fields["permissions"].queryset = filter_perms()

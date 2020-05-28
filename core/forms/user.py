# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission

from ..utils import filter_perms


# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------


class MyUserCreationForm(UserCreationForm):
    """Custom UserCreationForm."""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = [
            "password1",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "email",
            "username",
            "is_superuser",
            "groups",
            "user_permissions",
        ]

    def __init__(self, user, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user = user

        # filter out the permissions we don't want the user to see
        if not self.user.is_superuser:
            self.fields["user_permissions"].queryset = filter_perms()

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

            # UserCreationForm does NOT save groups or user_permissions
            # by default so we add back that functionality here
            for g in self.cleaned_data["groups"]:
                instance.groups.add(g)

            for p in self.cleaned_data["user_permissions"]:
                instance.user_permissions.add(p)

        return instance


class MyUserChangeForm(UserChangeForm):
    """Custom UserChangeForm."""

    class Meta(UserChangeForm.Meta):
        model = get_user_model()

    def __init__(self, user, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user = user

        # remove date_joined as we can't remove it by
        # specifying fields with a UserChangeForm
        del self.fields["date_joined"]

        # filter out the permissions we don't want the user to see
        # if not self.user.is_superuser:
        self.fields["user_permissions"].queryset = filter_perms()

    # def save(self, commit=True):
    #     instance = super().save(commit)
    #     return instance
 
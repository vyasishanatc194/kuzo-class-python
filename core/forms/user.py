# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group, Permission

from ..utils import filter_perms

from core.utils import Emails
from django.template import loader

# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------


class MyUserCreationForm(UserCreationForm):

    """
    Custom UserCreationForm.
    """

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = [
            "password1",
            "is_staff",
            "is_active",
            "email",
            "is_superuser",
            "user_permissions",
            "name",
            'customer_id',
                  
        ]


    def __init__(self, user, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user = user


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.username=instance.email
        instance.save()

        if commit:
            instance.save()

        return instance


class MyUserChangeForm(UserChangeForm):
    
    """
    Custom UserChangeForm.
    """

    class Meta(UserChangeForm.Meta):
        model = get_user_model()

        fields = [
            "is_staff",
            "is_active",
            "email",
            "is_superuser",
            "name",
            'customer_id',
          
                  
        ]

   
    def __init__(self, user, *args, **kwargs):

        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.user = user

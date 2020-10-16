from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth.models import Group
from allauth.account.adapter import app_settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from core.utils import CustomValidation, validate_password

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def clean_name(self, name):
        return name

    def clean_password(self, password, user=None):
        """
        Validates a password. You can hook into this if you want to
        restric the allowed password choices.
        """
        min_length = app_settings.PASSWORD_MIN_LENGTH
        if min_length and len(password) < min_length:
            msg = _("Password must be a minimum of {0} characters.").format(min_length)
            # raise forms.ValidationError(_("Password must be a minimum of {0} "
            #                               "characters.").format(min_length))
            raise CustomValidation(msg, status_code=status.HTTP_200_OK)

        validate_password(password, user)
        return password
        
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_username, user_email, user_field
 
        data = form.cleaned_data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        username = data.get('username')
        user_email(user, email)
        user_username(user, username)
    

        mobile = data.get('mobile')
        if mobile:
            user_field(user, 'mobile', mobile)
         
        city = data.get('city')
        if city:
            user_field(user, 'city', city)
      

        name = data.get('name')
        if name:
            user_field(user, 'name', name)


        role = data.get('role')
        if name:
            user_field(user, 'role', role)    

        dob = data.get('dob')
        if dob:
            user_field(user, 'dob', dob)

        avatar = data.get('avatar')
        # user.avatar = avatar
        # print('--------------------------avatar--------------------------')
        # print(avatar)
        if avatar:
            user_field(user, 'avatar', avatar)

        if first_name:
            user_field(user, 'first_name', first_name)
        if last_name:
            user_field(user, 'last_name', last_name)
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
 

        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()

            # group = Group.objects.get(name=user_type)
            # user.groups.add(group)

        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

#from .user_emp import User_Emp
from .users import User

from django.contrib.auth.models import Group

from django.conf import settings

from rest_framework.authtoken.models import Token as DefaultTokenModel

from core.utils import import_callable

# Register your models here.

TokenModel = import_callable(getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel))

from .card_payment import Card

from .charge import Charge





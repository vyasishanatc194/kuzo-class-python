from __future__ import print_function
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from allauth.account.signals import user_signed_up, email_confirmed
from .models import Account, Billing, Plan, Game


# @receiver(user_signed_up, dispatch_uid="user_signed_up")
# def create_new_profile(request, **kwargs):
#     if settings.DEBUG:
#         print('# ============ Signal fired: "user_signed_up" ============= #')
#     #if not request.user.is_authenticated:
#     #    return

#     user = kwargs['user']

#     # add user group User to Client User
#     g = Group.objects.get(name='User')
#     user.groups.add(g)

#     # Create a new Account For Client User
#     account = Account(user=user)
#     account.name = user.username
#     account.save()


#     game = Game(account=account)
#     game.name = 'Demo Game'
#     game.save()

#     plan = Plan.objects.get(default=True)

#     # Assign a Default Plan to Client User
#     billing = Billing(account=account)
#     billing.plan = plan
#     billing.email = user.email
#     billing.company_name = user.username
#     billing.save()

#     if settings.DEBUG:
#         print('New profile created for user ' + user.username)
#     return

#from __future__ import print_function
#from django.conf import settings
#from django.dispatch import receiver
#from django.contrib.auth import get_user_model, authenticate
#from django.contrib.auth.models import User, Group
#from allauth.account.signals import user_signed_up, email_confirmed
## from .models import Account, Billing, Plan, Game
#from core.utils import MyStripe, send_sms
#from django.db.models.signals import post_save
#from core.models import Otp
#import random as r
#import logging
#
#UserModel = get_user_model()
#
#@receiver(post_save, sender=UserModel)
#def save_profile(sender, instance, created, **kwargs):
#    if created:
#        print('# ============ Signal fired: "user_signed_up" ============= #')
#
#        print(instance)
#        stripe = MyStripe()
#        customer = stripe.createCustomer(instance)
#        print(customer)
#        customerId = customer.id
#        print('New profile created for user ' + instance.username)
#        instance.customer_id = customerId
#        instance.save()
#
#        # print('# ============ Create OTP AND SEND SMS" ============= #')
#        # 
#        # otp = ""
#        # for i in range(4):
#        #     otp += str(r.randint(1, 9))
#        # otp = int(otp)
#        #
#        # otp_data = {
#        #     "user": instance.id,
#        #     "phone": instance.mobile,
#        #     "otp": otp,
#        # }
#        # print(instance)
#        #
#        # Otp.objects.create(user=instance, mobile=instance.mobile, otp=otp)
        #
        # msg = f'Hi {instance} ! Your account verification code is : {otp}'
        # sms = send_sms(instance.mobile, msg)
        # logging.debug(sms)
        # print(sms)
        #
        # print('# ============ Create OTP AND SEND SMS END" ============= #')
      #  return


# @receiver(user_signed_up, dispatch_uid="user_signed_up")
# def create_new_profile(request, **kwargs):
#     if settings.DEBUG:
#         print('# ============ Signal fired: "user_signed_up" ============= #')
    
#     user = kwargs['user']
#     stripe = MyStripe()
#     print(user)
#     print(stripe.createCustomer())
    
#     if settings.DEBUG:
#         print('New profile created for user ' + user.username)
#     return
    


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

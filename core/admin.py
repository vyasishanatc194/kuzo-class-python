from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User, UserProfile, SubscriptionOrder


admin.site.register(User)

admin.site.register(UserProfile)

admin.site.register(SubscriptionOrder)




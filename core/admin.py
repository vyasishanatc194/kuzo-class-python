from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User, UserProfile, SubscriptionOrder, Card, Transactionlog, Event, EventClass, EventOrder


admin.site.register(User)

admin.site.register(UserProfile)

admin.site.register(SubscriptionOrder)

admin.site.register(Transactionlog)


admin.site.register(Card)

admin.site.register(Event)

admin.site.register(EventClass)
admin.site.register(EventOrder)




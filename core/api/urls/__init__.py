# -*- coding: utf-8 -*-
from django.urls import include, path
from django.conf.urls import url


from core.api.views import (
    MyRegisterView,
    LoginView,
    LogoutView,
    ProfileDetailsView,
    ProfileUpdateView,
    ChangeCurrentPassword,
    PasswordResetView,
    PasswordResetConfirmView,

) 

from . import billing_details

from .import subscribe_plan

from .import offer

from .import credit

from .import faq

from  core.api.views import BookEventAPI

from .import event

from .import event_class


urlpatterns = [

    # User Account 

    path('create-account/', MyRegisterView.as_view(), name='create-account'),    
    path('login/', LoginView.as_view(),name='core-auth-login'),
    path('logout/', LogoutView.as_view(),name='core-auth-logout'),
    path('profile-details/', ProfileDetailsView.as_view(),name='profile-details'),
    path('profile-update/', ProfileUpdateView.as_view(),name='user-update'),
    path('change-current-password/', ChangeCurrentPassword.as_view(),name='change-current-password'),
    path("billing-details/", include(billing_details)),
    path("subscribe-plan/", include(subscribe_plan)),
    path("forget-password/", PasswordResetView.as_view(), name="forget-password"),
    path("set-new-password/", PasswordResetConfirmView.as_view(), name="set-new-password"),
    path("influencer-offer/", include(offer)),
    path("credit/", include(credit)),
    path("faq/", include(faq)),
    path('book-event/', BookEventAPI.as_view(), name='book-event'),    
    path("event/", include(event)),
    path("event-class/", include(event_class)),

]





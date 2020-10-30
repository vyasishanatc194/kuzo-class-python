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
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
    ForgotPasswordAPIView,
    ChangePasswordLinkCheckAPIView,
    SetPasswordAPIView,

) 

from . import billing_details

from .import subscribe_plan

from .import offer

from .import credit

urlpatterns = [

    # User Account 

    path('create-account/', MyRegisterView.as_view(), name='create-account'),    
    path('login/', LoginView.as_view(),name='core-auth-login'),
    path('logout/', LogoutView.as_view(),name='core-auth-logout'),
    path('profile-details/<int:pk>', ProfileDetailsView.as_view(),name='profile-details'),
    path('profile-update/<int:pk>', ProfileUpdateView.as_view(),name='user-update'),
    path('change-current-password/', ChangeCurrentPassword.as_view(),name='change-current-password'),
    path("billing-details/", include(billing_details)),
    path("subscribe-plan/", include(subscribe_plan)),
    path("password/change/", PasswordChangeView.as_view(), name="change-password"),
    path("password/reset/", PasswordResetView.as_view(), name="reset-password"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="reset-password-confirm"),
    path("forget-password", ForgotPasswordAPIView.as_view(), name="forget-password"),
    url(r'^verify-link/(?P<uuid_string>.+)', ChangePasswordLinkCheckAPIView.as_view(), name= 'verify-link'),
    url(r'^set-new-password/(?P<uuid_string>.+)', SetPasswordAPIView.as_view(), name= 'set-new-password'),
    path("influencer-offer/", include(offer)),
    path("credit/", include(credit)),


]

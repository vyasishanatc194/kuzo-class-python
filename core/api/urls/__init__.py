# -*- coding: utf-8 -*-
from django.urls import include, path


from core.api.views import (
    MyRegisterView,
    LoginView,
    LogoutView,
    ProfileDetailsView,
    ProfileUpdateView

) 

from . import billing_details

from .import subscribe_plan

urlpatterns = [

    # User Account 

    path('create-account/', MyRegisterView.as_view(), name='create-account'),    
    path('login/', LoginView.as_view(),name='core-auth-login'),
    path('logout/', LogoutView.as_view(),name='core-auth-logout'),
    path('profile-details/<int:pk>', ProfileDetailsView.as_view(),name='profile-details'),
    path('profile-update/<int:pk>', ProfileUpdateView.as_view(),name='user-update'),
    path("billing-details/", include(billing_details)),
    path("subscribe-plan/", include(subscribe_plan)),


]

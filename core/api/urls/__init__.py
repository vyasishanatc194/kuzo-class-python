# -*- coding: utf-8 -*-
from django.urls import include, path


from core.api.views import LoginView, LogoutView, UserDetailsView, ProfileDetailsView, ProfileUpdateView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView

from . import (
    user,
    social_login,
    social_connect,
    card_payment,
    charge,
  
)


urlpatterns = [
     

    path("social-login/", include(social_login)),
    
    path("social-connect/", include(social_connect)),


    
    path('login/', LoginView.as_view(),name='core-auth-login'),

    path('logout/', LogoutView.as_view(),name='core-auth-logout'),



 
     path('profile/<int:pk>', ProfileDetailsView.as_view(),name='user-profile'),
 
     path('profile-update/<int:pk>', ProfileUpdateView.as_view(),name='user-update'),


    path("card_payment/", include(card_payment)),
#
    path("charge/", include(charge)),



    


]

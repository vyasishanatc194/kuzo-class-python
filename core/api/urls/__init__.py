# -*- coding: utf-8 -*-
from django.urls import include, path


from core.api.views import (
    MyRegisterView,
    LoginView,
    LogoutView,
    ProfileDetailsView

) 


urlpatterns = [


    path('create-account/', MyRegisterView.as_view(), name='create-account'),    
    path('login/', LoginView.as_view(),name='core-auth-login'),
    path('logout/', LogoutView.as_view(),name='core-auth-logout'),
    path('profile-details/<int:pk>', ProfileDetailsView.as_view(),name='profile-details'),
    # path('profile-update/<int:pk>', ProfileUpdateView.as_view(),name='user-update'),

]

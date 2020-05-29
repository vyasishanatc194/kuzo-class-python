# -*- coding: utf-8 -*-
from django.urls import include, path 
from . import user
from . import social_login
from . import social_connect




urlpatterns = [
     
    path("users/", include(user)),

    path("login/", include(social_login)),
    
    path("connect/", include(social_connect)),

]

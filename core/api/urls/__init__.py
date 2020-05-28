# -*- coding: utf-8 -*-
from django.urls import include, path
from . import user



urlpatterns = [
     
    path("users/", include(user)),
     
]

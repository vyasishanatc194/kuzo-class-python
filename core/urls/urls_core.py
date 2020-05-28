# -*- coding: utf-8 -*-

from django.urls import path,include
from django.views.generic import TemplateView
from . import views
  
app_name = "core"

urlpatterns = [

    path("", TemplateView.as_view(template_name="pages/home.html"), name="index"),

    # User
    path("users/", views.UserListView.as_view(), name="user-detail"),

    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/create/", views.UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
    path(
        "users/<int:pk>/password/",
        views.UserPasswordView.as_view(),
        name="user-password",
    ),
    path("ajax-users", views.UserAjaxPagination.as_view(), name="user-list-ajax"),
]
 

 
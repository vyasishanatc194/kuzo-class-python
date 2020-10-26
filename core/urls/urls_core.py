# -*- coding: utf-8 -*-

from django.urls import path, include
from django.views.generic import TemplateView
from . import views
app_name = "core"

urlpatterns = [

    path("", TemplateView.as_view(template_name="core/home.html"), name="index"),

    # User
    path("users/", views.UserListView.as_view(), name="user-detail"),

    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/create/", views.UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
    path("users/<int:pk>/password/", views.UserPasswordView.as_view(), name="user-password"),
    path("ajax-users", views.UserAjaxPagination.as_view(), name="user-list-ajax"),
]
 
urlpatterns += [
 

    path("test_mail", views.send_test_mail, name="send-test-mail" ),

    #plan
    path("subscription-plan/", views.SubscriptionPlanListView.as_view(), name="subscriptionplan-list"),
    path("subscription-plan/create/", views.SubscriptionPlanCreateView.as_view(), name="subscriptionplan-create"),
    path("subscription-plan/<int:pk>/update/", views.SubscriptionPlanUpdateView.as_view(), name="subscriptionplan-update"),
    path("subscription-plan/<int:pk>/delete/", views.SubscriptionPlanDeleteView.as_view(), name="subscriptionplan-delete"),
    path("ajax-subscription-plan", views.SubscriptionPlanAjaxPagination.as_view(), name="subscriptionplan-list-ajax"),
   
    #offer

    path("offer/", views.OfferListView.as_view(), name="offer-list"),
    path("offer/create/", views.OfferCreateView.as_view(), name="offer-create"),
    path("offer/<int:pk>/update/", views.OfferUpdateView.as_view(), name="offer-update"),
    path("offer/<int:pk>/delete/", views.OfferDeleteView.as_view(), name="offer-delete"),
    path("ajax-offer", views.OfferAjaxPagination.as_view(), name="offer-list-ajax"),

    
    path("banner/", views.BannerListView.as_view(), name="banner-list"),
    path("banner/create/", views.BannerCreateView.as_view(), name="banner-create"),
    path("banner/<int:pk>/update/", views.BannerUpdateView.as_view(), name="banner-update"),
    path("banner/<int:pk>/delete/", views.BannerDeleteView.as_view(), name="banner-delete"),
    path("ajax-banner", views.BannerAjaxPagination.as_view(), name="banner-list-ajax"),
   

]


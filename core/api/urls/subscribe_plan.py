from django.urls import  path
from core.api.views.subscribe_plan import (
    SubscriptionPlanListAPIView,
    SubscriptionPlanPurchaseAPI,
    NewSubscriptionPlanPurchaseAPI
)

urlpatterns = [

    path("", SubscriptionPlanListAPIView.as_view(), name="subscribe-plan-list"),
    path("add/", SubscriptionPlanPurchaseAPI.as_view(), name="subscribe-plan-purchase"),
    path("new/", NewSubscriptionPlanPurchaseAPI.as_view(), name="subscribe-plan-new"),

]

from django.urls import  path
from core.api.views.influencer_payout import (
    StripeAccountCreateAPI,
    StripeTransferMoneyCreateAPI,
    PayoutHistoryAPIView,
    StripeAccountConnectAPI,
    StripeAccountLoginAPI,
    StripeAccountDiscoonectAPI,

)

urlpatterns = [

    path("create-stripe-account", StripeAccountCreateAPI.as_view(), name="create-stripe-account"),
    path("transfer-stripe-money", StripeTransferMoneyCreateAPI.as_view(), name="transfer-stripe-money"),
    path("history", PayoutHistoryAPIView.as_view(), name="payout-history"),
    path("stripe-connect", StripeAccountConnectAPI.as_view(), name="stripe-connect"),
    path("stripe-login", StripeAccountLoginAPI.as_view(), name="stripe-login"),
    path("stripe-disconnect", StripeAccountDiscoonectAPI.as_view(), name="stripe-disconnect"),

]

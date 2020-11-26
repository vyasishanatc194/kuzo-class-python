from django.urls import  path
from core.api.views.influencer_payout import (
    StripeAccountCreateAPI,
    StripeTransferMoneyCreateAPI,
    PayoutHistoryAPIView,

)

urlpatterns = [

    path("create-stripe-account", StripeAccountCreateAPI.as_view(), name="create-stripe-account"),
    path("transfer-stripe-money", StripeTransferMoneyCreateAPI.as_view(), name="transfer-stripe-money"),
    path("history", PayoutHistoryAPIView.as_view(), name="payout-history"),
]

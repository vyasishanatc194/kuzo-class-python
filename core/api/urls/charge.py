from django.urls import path
from core.api.views.charge import (
    ChargeCreateAPI,

)

urlpatterns = [

    path("create/", ChargeCreateAPI.as_view(), name="charge-create"),
]

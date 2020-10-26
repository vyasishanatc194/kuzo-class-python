from django.urls import  path
from core.api.views.card_payment import (
    CardAPIView,
    CardCreateAPI,
    CardDeleteAPIView,

)

urlpatterns = [

    path("<int:pk>", CardAPIView.as_view(), name="card-list"),
    path("create/", CardCreateAPI.as_view(), name="card-create"),
    path('delete/<int:pk>', CardDeleteAPIView.as_view(), name='card-delete'),
]

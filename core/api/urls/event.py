from django.urls import  path
from core.api.views.event import (
    EventAPIView,
    EventCreateAPI,
    EventUpdateAPI,
    EventDeleteAPI,
    HomePageEventListAPIView


)

urlpatterns = [

    path("", EventAPIView.as_view(), name="event-list"),
    path("create/", EventCreateAPI.as_view(), name="event-create"),
    path('update/<int:pk>', EventUpdateAPI.as_view(), name='event-update"'), 
    path('delete/<int:pk>', EventDeleteAPI.as_view(), name='event-delete"'), 
    path("home-page/", HomePageEventListAPIView.as_view(), name="event-list"),
    
]

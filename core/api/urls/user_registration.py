from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.api.views.user import AccountCreateApiView, UserOtpVerificationAPIView
 
urlpatterns = [
    
    path("user-create/",AccountCreateApiView.as_view(),name="user-create"),
    path('verify/<int:pk>', UserOtpVerificationAPIView.as_view(), name='verify'),

]
 
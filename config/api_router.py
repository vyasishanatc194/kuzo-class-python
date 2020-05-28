from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from core.api import urls

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"
 
urlpatterns = [
    path("auth-token/", obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path("swagger/", get_swagger_view(title="Night Market API")),
    
    path("users/", include(urls)),
]
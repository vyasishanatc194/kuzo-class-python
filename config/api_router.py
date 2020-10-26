from django.conf import settings
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_auth.registration.views import SocialAccountListView, SocialAccountDisconnectView 



from core.api import urls
 

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"
 
urlpatterns = [ 
    
    # path("auth-token/", obtain_jwt_token),

    path('api-token-refresh/', refresh_jwt_token),

    path('rest-auth/', include('rest_auth.urls')),

    
    
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    
    path(
        'socialaccounts/',
        SocialAccountListView.as_view(),
        name='social_account_list'
    ),
    re_path(
        r'^socialaccounts/(?P<pk>\d+)/disconnect/$',
        SocialAccountDisconnectView.as_view(),
        name='social_account_disconnect'
    ),

    path("swagger/", get_swagger_view(title="Inrelay API")),

    
    
    path('', include(urls)),
]

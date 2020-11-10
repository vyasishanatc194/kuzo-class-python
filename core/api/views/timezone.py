from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Banner
from core.api.apiviews import MyAPIView
from core.api.serializers import TimezoneSerializer

import pytz 
from pytz import timezone
# .................................................................................
# banner Plan API
# .................................................................................


class TimezoneListAPIView(MyAPIView):

    """
    API View for banner  listing
    """

    permission_classes = (AllowAny,)
    serializer_class = TimezoneSerializer

    def get(self, request, format=None):    
        get_imezone = pytz.common_timezones

        return Response({"status": "OK", "message": "Successfully fetched timezone list", "data": get_imezone})


    
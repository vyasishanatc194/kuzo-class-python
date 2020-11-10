from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import UserProfile, Event
from core.api.apiviews import MyAPIView
from core.api.serializers import InfluencerDetailsListSerializer


# .................................................................................
# InfluencerDetailsListAPIViewAPI
# .................................................................................


class InfluencerDetailsListAPIView(MyAPIView):

    """
    API View for banner  listing
    """

    permission_classes = (AllowAny,)
    serializer_class = InfluencerDetailsListSerializer

    def get(self, request, pk, format=None):  
        try:
            user_obj = Event.objects.filter(id=pk).first()
            influencer = UserProfile.objects.filter(user__id=user_obj.user.id)
            serializer = self.serializer_class(influencer, many=True, context={"request": request})

            new_serializer_data = list(serializer.data)
            new_serializer_data.append({'current_event_id': pk})

            return Response({"status": "OK", "message": "Successfully fetched influencer details ", "data": new_serializer_data})


        except Event.DoesNotExist:
            return Response({"status": "FAIL", "message": "Event not found", "data": []})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.api.pagination import CustomPagination

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Charge
from core.api.serializers import ChargeSerializer
from core.api.apiviews import MyAPIView
from core.utils import MyStripe, create_charge_object
import json

# .................................................................................
# Charge API
# .................................................................................

'''
class ChargeAPIView(MyAPIView):
    """API View for Charge listing"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ChargeSerializer

    def get(self, request, pk, format=None):
        """GET method for retrieving the data"""

        if request.user.is_authenticated:

            """ use user id """

            try:
                charges = Charge.objects.filter(user_id=pk)

                if charges is not None:
                    serializer = ChargeSerializer(charges, many=True, context={"request": request})
                    return Response({"message": "Successfully fetched charges", "data": serializer.data})

            except Charge.DoesNotExist:
                return Response({"message": "Charges not found"})

        else:
            return Response({"message": "Unauthorised User"})
'''


class ChargeCreateAPI(MyAPIView):
    
    """
    API View to create Charge
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ChargeSerializer
    queryset = Charge.objects.all()

    def post(self, request, format=None):
        """POST method to create the data"""

        if request.user.is_authenticated:
            try:
                stripe = MyStripe()
                newcharge = stripe.createCharge(request.data, request.data["card_id"], request.user.customer_id)

                data = create_charge_object(newcharge, request)

                serializer = ChargeSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()

                    return Response({"status": "OK", "message": "Successfully created charge", "data": serializer.data})

                else:
                    return Response({"status": "FAIL", "message": "Cannot create charge", "data": serializer.errors})

            except Exception as inst:
                print(inst)
                return Response({"status": "FAIL", "message": "Bad request", "data": []})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})

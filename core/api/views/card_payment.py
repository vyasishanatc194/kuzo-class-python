from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core.api.pagination import CustomPagination

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Card
from core.api.serializers import CardSerializer
from core.api.apiviews import MyAPIView
from core.utils import MyStripe, create_card_object

# .................................................................................
# Credit/Debit Card API
# .................................................................................


class CardAPIView(MyAPIView):
    """
    API View for Card listing
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    def get(self, request, pk, format=None):
        """GET method for retrieving the data"""

        if request.user.is_authenticated:

            """ use user id """

            try:
                cards = Card.objects.filter(user_id=pk)

                if cards is not None:
                    serializer = CardSerializer(cards, many=True, context={"request": request})
                    return Response({"status": "OK", "message": "Successfully fetched cards", "data": serializer.data})

            except Card.DoesNotExist:
                return Response({"status": "FAIL", "message": "Cards not found", "data": []})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class CardCreateAPI(MyAPIView):
    """API View to create Card"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer
    queryset = Card.objects.all()

    def post(self, request, format=None):
        """POST method to create the data"""

        if request.user.is_authenticated:
            try:
                print("***** Before Serializer *****")
                stripe = MyStripe()
                newcard = stripe.createCard(request.user.customer_id, request.data)

                data = create_card_object(newcard, request)

                serializer = CardSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()

                    return Response({"status": "OK", "message": "Successfully created card", "data": []})

                else:
                    return Response({"status": "FAIL", "message": "Cannot create card", "data": serializer.errors})

            except Exception as inst:
                print(inst)
                return Response({"status": "FAIL", "message": "Bad request", "data": []})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})


class CardDeleteAPIView(MyAPIView):
    """API View to delete Card"""

    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk, format=None):
        """DELETE method to delete the data"""

        if request.user.is_authenticated:
            try:
                cards = Card.objects.get(id=pk)
                stripe = MyStripe()
                stripe.deleteCard(request.user.customer_id, cards.card_id)
                cards.delete()
                return Response({"status": "OK", "message": "Successfully deleted registered card", "data": []})

            except Card.DoesNotExist:
                return Response({"status": "FAIL", "message": "Registered Card not found", "data": []})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})

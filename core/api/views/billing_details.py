from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core.api.pagination import CustomPagination

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Card, User
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

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:
            stripe = MyStripe()

            """ Create Customer """

            if not request.user.customer_id:

                new_stripe_customer = stripe.createCustomer(request.user)
                
                User.objects.filter(id=request.user.id).update(customer_id=new_stripe_customer['id'])



            """ Add Card """

            new_card = stripe.createCard(request.user.customer_id, request.data)

            data = {
                "stripe_card_id":new_card['id'],
                "last4":new_card['last4'],
                "card_expiration_date": "{0}/{1}".format(new_card['exp_month'], new_card['exp_year']),
                "user":request.user.id,
            }


            check_card = Card.objects.filter(user__id=request.user.id).first()

            if check_card:

                """ Remove old card from stripe """

                stripe.deleteCard(request.user.customer_id, check_card.stripe_card_id)
                Card.objects.filter(user__id=request.user.id).update(**data)
                return Response({"status": "OK", "message": "Successfully Updated billing details", "data": []})


            else:    

                serializer = CardSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "OK", "message": "Successfully Updated billing details", "data": []})

                else:
                    return Response({"status": "FAIL", "message": "Cannot create card", "data": serializer.errors})

          

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})



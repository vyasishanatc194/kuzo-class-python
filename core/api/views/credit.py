from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core.api.pagination import CustomPagination

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Card, User,CreditOrder, UserProfile, Transactionlog, Credit
from core.api.apiviews import MyAPIView
from core.utils import MyStripe, create_card_object
import stripe as stripeErr
from core.api.serializers import CreditSerializer, TransactionlogSerializer


# .................................................................................
# Credit Plan API
# .................................................................................


class CreditListAPIView(MyAPIView):

    """
    API View for Credit  listing
    """

    permission_classes = (AllowAny,)
    serializer_class = CreditSerializer

    def get(self, request, format=None):    

        try:
            credit = Credit.objects.all()
            serializer = self.serializer_class(credit, many=True, context={"request": request})
            return Response({"status": "OK", "message": "Successfully fetched credit list", "data": serializer.data})

        except:
            return Response({"status": "FAIL", "message": "Credit plan not found", "data": []})




class CreditPurchaseAPI(MyAPIView):

    """API View to create Card"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:

            try:

                stripe = MyStripe()
                user_obj = User.objects.filter(id=request.user.id).first()
                user_plan = UserProfile.objects.filter(user__id=request.user.id).first()
                credit_obj = Credit.objects.filter(id=request.data['credit']).first()

                data = {
                    'source':request.data['stripe_token']
                }

                if not request.user.customer_id:
                    new_stripe_customer = stripe.createCustomer(request.user)
                    user_obj.customer_id = new_stripe_customer['id']
                    user_obj.save()

                new_card = stripe.createCard(user_obj.customer_id, data)
                transaction = stripe.createCharge(credit_obj.price, new_card, user_obj.customer_id)

                transaction_data = {

                        "user": request.user,
                        "transaction_type" : 'credit',
                        "amount" : credit_obj.price,
                        "credit": credit_obj.number_of_credit,
                        "types": "credit",
                        "transaction_status": "success" ,   
                        "transaction_id":transaction['id'] ,       

                    }

                credit_order_data = {

                    "user": request.user,
                    "credit" : credit_obj,
                    "amount" : credit_obj.price,

                }
                ob=Transactionlog.objects.create(**transaction_data)
                CreditOrder.objects.create(**credit_order_data)
                user_plan.credit = credit_obj.number_of_credit
                user_plan.save()
                serilizer = TransactionlogSerializer(ob)

                return Response({"status": "OK", "message": "Successfully purchased credit", "data": serilizer.data})
                    
            except stripeErr.error.CardError as e:
                body = e.json_body
                err  = body.get('error', {})

                return Response({"status": "FAIL", "message": err['message'], "data": []})

            except stripeErr.error.AuthenticationError as e:

                body = e.json_body
                err  = body.get('error', {})
                return Response({"status": "FAIL", "message": err['message'], "data": []})

    
            except stripeErr.error.InvalidRequestError  as e:
                body = e.json_body
                err  = body.get('error', {})
                return Response({"status": "FAIL", "message": err['message'], "data": []})

            except Exception as e:

                return Response({"status": "FAIL", "message": str(e), "data": []})

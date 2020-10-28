from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core.api.pagination import CustomPagination

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Card, User, SubscriptionPlan, UserProfile
from core.api.serializers import CardSerializer, SubscriptionPlanSerializer, TransactionlogSerializer, SubscriptionOrderSerializer
from core.api.apiviews import MyAPIView
from core.utils import MyStripe, create_card_object


# .................................................................................
# Subscription Plan API
# .................................................................................


class SubscriptionPlanListAPIView(MyAPIView):

    """
    API View for Subscription Plan listing
    """

    permission_classes = (AllowAny,)
    serializer_class = SubscriptionPlanSerializer

    def get(self, request, format=None):    

        try:
            plan = SubscriptionPlan.objects.all()
            serializer = self.serializer_class(plan, many=True, context={"request": request})
            return Response({"status": "OK", "message": "Successfully fetched subscription plan list", "data": serializer.data})

        except Card.DoesNotExist:
            return Response({"status": "FAIL", "message": "Subscription plan not found", "data": []})

import datetime
from dateutil import relativedelta

class SubscriptionPlanPurchaseAPI(MyAPIView):

    """API View to create Card"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:

            nextmonth = datetime.datetime.today() + relativedelta.relativedelta(months=1)


            stripe = MyStripe()

            check_plan = UserProfile.objects.filter(user__id=request.user.id).first()

            
            # card_ob = Card.objects.get(user__id=request.user.id)

            subscription = SubscriptionPlan.objects.filter(id=request.data['subscription']).first()

            sub_obj = stripe.subscribePlan(request.user.customer_id, subscription.stripe_plan_id)


            subscripton_data = {
                    "user":request.user.id,
                    "subscription": request.data['subscription'],
                    "amount": request.data['amount'],
                    "charge_id": sub_obj['id'],
                    "ordre_status":"success",
                    "expire_date": nextmonth,   
            }

            transaction_data = {

                "user": request.user.id,
                "transaction_type" : 'subscription',
                "amount" : request.data['amount'],
                "credit": subscription.number_of_credit,
                "types": "credit",
                "transaction_status": "success" ,   
                "transaction_id":sub_obj['id'] ,       

            }

            subscription_serilzer = SubscriptionOrderSerializer(data=subscripton_data) 

            if subscription_serilzer.is_valid():
                subscription_serilzer.save()


            transactoion_serilzer = SubscriptionOrderSerializer(data=subscripton_data) 
            
            if transactoion_serilzer.is_valid():
                transactoion_serilzer.save()

            check_plan.credit =  float(check_plan.credit) + float(subscription.number_of_credit)
            check_plan.subscription = subscription.id
            check_plan.save()

            return Response({"status": "OK", "message": "Changed plan successfully", "data": subscription_serilzer.data})



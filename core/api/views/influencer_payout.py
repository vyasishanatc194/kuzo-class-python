import stripe
import time
from django.conf import settings
from core.api.apiviews import MyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import InfluencerTransferredMoney, EventOrder, User
from core.api.serializers import InfluencerTransferredMoneySerializer


stripe.api_key = settings.API_KEY


class StripeAccountCreateAPI(MyAPIView):

    """API View to create offer"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        """POST method to offer the data"""

        if request.user.is_authenticated:
            request.data._mutable = True
            email=request.user.email       
            create_acc=stripe.Account.create(
            type="custom",
            country=request.data['country'],
            business_type="individual",

            business_profile = {"url": request.data['website_url']},

            individual={
                "dob":{"day":"01","month":"12","year":"1997",},
                "first_name":request.data['first_name'],
                "last_name":request.data['last_name'],
                "phone":request.data['phone'],
                "email":email,
                "ssn_last_4":request.data['ssn_last_4'],
                "address":{"city":request.data['city'], "country":request.data['country'], "line1":request.data['address1'], "postal_code":request.data['postal_code'], "state": request.data['state']}
            },
            email=email,
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            },

            external_account={
                "object":"bank_account",
                "country": request.data['country'],
                "currency":request.data['currency'],
                "account_holder_name": "{0} {1}".format(request.data['first_name'],request.data['last_name'] ),
                "account_holder_type":"individual",
                "account_number":request.data['account_number'],
                "routing_number":request.data['routing_number'],
            },
            settings = {
                "payouts":{"schedule":{"interval":"weekly", "weekly_anchor":"sunday"}}
            },
            tos_acceptance={
                'date': int(time.time()),
                'ip': '8.8.8.8', 
            }
            )

            return Response({"status": "OK", "message": "Successfully created event", "data": create_acc.id})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})



class StripeTransferMoneyCreateAPI(MyAPIView):

    """API View to create offer"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        """POST method to offer the data"""

        if request.user.is_authenticated:
            
            if request.user.influencer_stripe_account_id:
                
                if request.user.earned_money < 1:
                    return Response({"status": "OK", "message": "You have not enough amount to transfer", "data": []})

                transaction=stripe.Transfer.create(
                amount=int(request.user.earned_money)*100,
                currency="usd",
                destination= str(request.user.influencer_stripe_account_id),
                )

                User.objects.filter(id=request.user.id).update(earned_money=0)

                transfer = {
                    "user": request.user.id,
                    "amount": int(request.user.earned_money),
                    "status":"success",
                    "transaction_id":transaction.id,
                }

                serializer = InfluencerTransferredMoneySerializer(data=transfer)
                if serializer.is_valid():
                    serializer.save()
        
                    return Response({"status": "OK", "message": "Successfully transfered money", "data": serializer.data})
                else:
                    return Response({"status": "OK", "message": "Serializer errors", "data": serializer.errors})

            
            else:
                return Response({"status": "OK", "message": "Please create stripe account & update into kuzo account", "data": []})
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})



class PayoutHistoryAPIView(MyAPIView):

    """
    API View for transaction history
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = InfluencerTransferredMoneySerializer

    def get(self, request):

        if request.user.is_authenticated:

            transaction_history = InfluencerTransferredMoney.objects.filter(user__id=request.user.id).order_by("-created_at")
            serializer = self.serializer_class(
                transaction_history, many=True, context={"request": request}
            )
            return Response(
                {
                    "status": "OK",
                    "message": "Successfully fetched transaction history",
                    "data": serializer.data,
                }
            )
        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})

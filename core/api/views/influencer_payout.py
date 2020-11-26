import stripe
import time
from django.conf import settings
from core.api.apiviews import MyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


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

            request.data._mutable = True
            stripe.Transfer.create(
            amount=400,
            currency="usd",
            destination="acct_1HrLKjQmr4yatsZX",
            
            )

            return Response({"status": "OK", "message": "Successfully transfered money", "data": []})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})

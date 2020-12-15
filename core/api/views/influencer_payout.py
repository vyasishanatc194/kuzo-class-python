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


            front_file = request.data['front']
            back_file = request.data['back']


            front=stripe.File.create(purpose="identity_document",file=front_file)
            back=stripe.File.create(purpose="identity_document",file=back_file)


            email=request.user.email       
            create_acc=stripe.Account.create(
            type="custom",
            country=request.data['country'],
            business_type="individual",

            business_profile = {"url": request.data['website_url'], "mcc":"1520"},

            individual={
                "dob":{"day":"01","month":"12","year":"1997",},
                "first_name":request.data['first_name'],
                "last_name":request.data['last_name'],
                "phone":request.data['phone'],
                "email":email,
                "id_number":"012345789",
                "verification": {"document": {"front": front['id'], "back":back['id']}},
                "address":{"line1":request.data['address1'],"line2":request.data['address1'], "city":request.data['city'], "state": request.data['state'], "postal_code":request.data['postal_code'],"country":request.data['country']}
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
            ob=User.objects.filter(id=request.user.id).first()
            ob.influencer_stripe_account_id = create_acc.id
            ob.save()

            return Response({"status": "OK", "message": "Successfully created event", "data": create_acc.id})

        else:
            return Response({"status": "FAIL", "message": "Unauthorised User", "data": []})



class StripeAccountConnectAPI(MyAPIView):

    """API View to create offer"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        """POST method to offer the data"""

        if request.user.is_authenticated:

            try:
                
                account = stripe.Account.create(
                        type='express',
                     )   

                ob=User.objects.filter(id=request.user.id).first()
                ob.influencer_stripe_account_id = account.id
                ob.save()

                account_links = stripe.AccountLink.create(
                    account=account.id,
                    refresh_url='http://44.225.113.133/influencer-earned',
                    return_url='http://44.225.113.133/influencer-earned',
                    type='account_onboarding',
                )

                return Response({"status": "OK", "message": "Successfully connected stripe account", "data": account_links})

            except Exception as e:
                return Response({"status": "FAIL", "message": str(e), "data": []})
       
       
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

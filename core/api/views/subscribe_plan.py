from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core.api.pagination import CustomPagination

from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Card, User, SubscriptionPlan, UserProfile, SubscriptionOrder, Transactionlog, Event, EventOrder
from core.api.serializers import CardSerializer, EventOrderSerializer, SubscriptionPlanSerializer, TransactionlogSerializer, SubscriptionOrderSerializer
from core.api.apiviews import MyAPIView
from core.utils import MyStripe, create_card_object
import stripe as stripeErr
import datetime
from dateutil import relativedelta
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



class SubscriptionPlanPurchaseAPI(MyAPIView):

    """API View to create Card"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:

            nextmonth = datetime.datetime.today() + relativedelta.relativedelta(months=1)


            stripeErr.api_key = "sk_test_M59oeSkIQEUMGT9MEXaFgTzX00Wy4c7Ptb"

            stripe = MyStripe()

            user_plan = UserProfile.objects.filter(user__id=request.user.id).first()

            subscription = SubscriptionPlan.objects.filter(id=request.data['subscription']).first()

            """ Stripe call for subscription """

            try:

                subscribe_new_plan = stripe.subscribePlan(request.user.customer_id, subscription.stripe_plan_id, payment_method.id)
                
                if subscribe_new_plan:

                    subscripton_data = {
                            "user":request.user,
                            "subscription": subscription,
                            "amount": request.data['amount'],
                            "charge_id": subscribe_new_plan['id'],
                            "ordre_status":"success",
                            "plan_status":"active",
                            "stripe_subscription_id":subscribe_new_plan['id'],
                            "expire_date": nextmonth,   
                    }

                    transaction_data = {

                        "user": request.user,
                        "transaction_type" : 'subscription',
                        "amount" : request.data['amount'],
                        "credit": subscription.number_of_credit,
                        "types": "credit",
                        "transaction_status": "success" ,   
                        "transaction_id":subscribe_new_plan['id'] ,       

                    }
            
                    user_plan.credit =  float(user_plan.credit) + float(subscription.number_of_credit)
                    user_plan.subscription = subscription
                    user_plan.save()

                    subscription_order = SubscriptionOrder.objects.filter(user__id=request.user.id, plan_status='active').first()
                    
                    """ Cancel old plan """

                    stripe.CancelSubscriptionPlan(subscription_order.stripe_subscription_id)
                    subscription_order.plan_status = 'cancel'
                    subscription_order.save()

                    SubscriptionOrder.objects.create(**subscripton_data)
                    Transactionlog.objects.create(**transaction_data)

                   

                    return Response({"status": "OK", "message": "Changed plan successfully", "data": []})


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


class NewSubscriptionPlanPurchaseAPI(MyAPIView):

    """API View to create Card"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    def post(self, request, format=None):

        """POST method to create the data"""

        if request.user.is_authenticated:

            nextmonth = datetime.datetime.today() + relativedelta.relativedelta(months=1)

            stripe = MyStripe()

            user_obj = User.objects.filter(id=request.user.id).first()
            user_plan = UserProfile.objects.filter(user__id=request.user.id).first()
            subscription = SubscriptionPlan.objects.filter(id=request.data['subscription']).first()
            event = Event.objects.filter(id=request.data['event']).first()

            check_participant = EventOrder.objects.filter(user__id=request.user.id, event__id=event.id).exists()

            if check_participant:

                return Response({"status": "OK", "message": "You have already participated in this event", "data": []})

            # Check stripe customer id 

            if not request.user.customer_id:
                new_stripe_customer = stripe.createCustomer(request.user)
                user_obj.customer_id = new_stripe_customer['id']
                user_obj.save()

            # New Subscription & event registration

            if request.data['is_subscription_access']=='true':

                if user_plan.subscription:

                    if int(user_plan.credit) < int(event.credit_required):

                        return Response({"status": "OK", "message": "Please Change your current subscriptin plan or buy more credit.", "data": []})

                    else:

                        event_order_data = {

                            "user": request.user,
                            "event" : event,
                            "used_credit" : event.credit_required,
                            "order_status": "success",
                            "charge_id": "credit used",

                        }

                        event.remianing_spots = int(event.remianing_spots) + 1
                        event.save()
                        event_new = EventOrder.objects.create(**event_order_data)

                        transaction_data = {

                                "user": request.user,
                                "transaction_type" : 'credit',
                                "amount" : event.price,
                                "credit": event.credit_required,
                                "types": "debit",
                                "transaction_status": "success" ,   
                                "transaction_id": event_new.id,       

                        }

                        Transactionlog.objects.create(**transaction_data)
                        user_plan.credit =  int(user_plan.credit)  - int(event.credit_required)
                        user_plan.save()
                        serilzer = EventOrderSerializer(event_new)
                        return Response({"status": "OK", "message": "Event registration  process completed successfully", "data": serilzer.data})


                try:
                    if event.credit_required  > subscription.number_of_credit:

                        return Response({"status": "OK", "message": "This Plan is not enought for this event.Please choose another plan.", "data": []})


                    payment_method = stripe.CreatePaymentMethod(request.data['stripe_token'])

                    Card.objects.create(user=user_obj, stripe_card_id=payment_method.id, last4=payment_method['card']['last4'], card_expiration_date='{0}/{1}'.format(payment_method['card']['exp_month'], payment_method['card']['exp_year']))

                    stripe.PaymentMethodAttach(payment_method.id, user_obj.customer_id)
                
                    subscribe_new_plan = stripe.subscribePlan(user_obj.customer_id, subscription.stripe_plan_id, payment_method.id)
                    
            
                    if subscribe_new_plan['status']=='active':

                        subscripton_data = {
                                "user":request.user,
                                "subscription": subscription,
                                "amount": subscription.price,
                                "charge_id": subscribe_new_plan['id'],
                                "ordre_status":"success",
                                "plan_status":"active",
                                "stripe_subscription_id":subscribe_new_plan['id'],
                                "expire_date": nextmonth,   
                        }

                        event_order_data = {

                            "user": request.user,
                            "event" : event,
                            "used_credit" : event.credit_required,
                            "order_status": "success",
                            "charge_id": "credit used",

                        }

                        user_plan.credit =  int(user_plan.credit) + int(subscription.number_of_credit) - int(event.credit_required)
                        user_plan.subscription = subscription
                        user_plan.save()

                        event.remianing_spots = int(event.remianing_spots) + 1
                        event.save()

                        subscription_new = SubscriptionOrder.objects.create(**subscripton_data)


                        transaction_data = {

                            "user": request.user,
                            "transaction_type" : 'subscription',
                            "amount" : subscription.price,
                            "credit": subscription.number_of_credit,
                            "types": "credit",
                            "transaction_status": "success" ,   
                            "transaction_id": subscription_new.id ,       

                        }
                        Transactionlog.objects.create(**transaction_data)
                        event_new = EventOrder.objects.create(**event_order_data)

                        event_transaction_data = {

                            "user": request.user,
                            "transaction_type" : 'credit',
                            "amount" : event.price,
                            "credit": event.credit_required,
                            "types": "debit",
                            "transaction_status": "success" ,   
                            "transaction_id": event_new.id,       
                        }

                        Transactionlog.objects.create(**event_transaction_data)

                        serilzer = EventOrderSerializer(event_new)
                        return Response({"status": "OK", "message": "Subscription & event registration process completed successfully", "data": serilzer.data})

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

            else:

                try:

                    data={
                        'source':request.data['stripe_token']
                    }

                    new_card = stripe.createCard(user_obj.customer_id, data)

                    transaction = stripe.createCharge(event.price, new_card, user_obj.customer_id)

                    event_order_data = {

                        "user": request.user,
                        "event" : event,
                        "used_credit" : event.credit_required,
                        "charge_id":transaction['id'],
                        "order_status": "success",

                    }

                    event_new = EventOrder.objects.create(**event_order_data)


                    transaction_data = {

                            "user": request.user,
                            "transaction_type" : 'direct_purchase',
                            "amount" : event.price,
                            "credit": event.credit_required,
                            "types": "debit",
                            "transaction_status": "success" ,   
                            "transaction_id": event_new.id,       

                        }

                    event.remianing_spots = int(event.remianing_spots) + 1
                    event.save()
                    Transactionlog.objects.create(**transaction_data)

                    serializer = EventOrderSerializer(event_new)

                    return Response({"status": "OK", "message": "Event registration process completed successfully", "data": serializer.data})
                
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

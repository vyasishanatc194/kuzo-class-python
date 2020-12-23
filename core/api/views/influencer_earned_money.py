from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
import stripe

from core.api.apiviews import MyAPIView
from core.utils.daily_earning_money import daily_earning

from core.models import EventOrder

current_datetime =  datetime.now()
current_datetime += timedelta(days=1)

# .................................................................................
# InfluencerEarnMoneyListAPIView Plan API
# .................................................................................


class InfluencerEarnMoneyListAPIView(MyAPIView):

    """
    API View for banner  listing
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        try:

            data = {}
            result =[]
            day=0

            if request.user.influencer_stripe_account_id:
                new_result = stripe.Account.retrieve(str(request.user.influencer_stripe_account_id))
                data['next_payout'] = new_result['settings']['payouts']

            search = request.GET["q"]

            if search == "month":
                day=30
                start_date = datetime.now() - timedelta(days = day)

            elif search == 'year':
                day=365
                start_date = datetime.now() - timedelta(days = day)

            elif search == 'week':
                day=7
                start_date = datetime.now() - timedelta(days = day)

            event = EventOrder.objects.filter(created_at__range=[start_date, current_datetime], event__user__id=request.user.id)
            total=event.aggregate(Sum('event__price'))
            data['total_earning'] = total['event__price__sum']
            data['total_enroll_student'] = event.count()
            res=daily_earning(request.user.id, start_date, day)
            data['daily_earning'] = res
            result.append(data)

            return Response(
                {
                    "status": "OK",
                    "message": "Successfully fetched data",
                    "data": result,
                }
            )

        except:
            return Response(
                    {
                        "status": "FAIL",
                        "message": "Bad request",
                        "data": [],
                    }
                )

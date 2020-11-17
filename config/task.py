from core.models import SubscriptionOrder, UserProfile
from core.utils import MyStripe
from . celery_app import *
from datetime import datetime
from dateutil import relativedelta


today = datetime.now().date()

import datetime
nextmonth = datetime.datetime.today() + relativedelta.relativedelta(months=1)


@app.task
def Update_credit():

    check_active_plan = SubscriptionOrder.objects.filter(plan_status="active", expire_date=today)

    try:
        for obj in check_active_plan:
            if obj.plan_status=="active":
                get_user_profile = UserProfile.objects.filter(user__id=obj.user.id).first()
                if get_user_profile.subscription:
                    stripe = MyStripe()
                    check_stripe_status = stripe.RetrieveSubscription(get_user_profile.stripe_subscription_id)
                    
                    check_invoice = stripe.InvoiceStatus(check_stripe_status['latest_invoice'])
                    
                    if check_stripe_status.status=="active" and check_invoice['status']=='paid':
                        get_user_profile.credit = int(get_user_profile.credit) + int(get_user_profile.subscription.number_of_credit)
                        get_user_profile.save()
                        obj.expire_date=nextmonth
                        obj.save()

                    return 'Updated successfully'

    except:
        return 'Error'
   
  
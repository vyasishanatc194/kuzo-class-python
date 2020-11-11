from core.models import SubscriptionOrder


def my_scheduled_job():
    ob=SubscriptionOrder.objects.all()
    print(ob)
    return 'code updated successfully'

  
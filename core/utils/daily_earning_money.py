from datetime import timedelta
from django.db.models import Sum

from core.models.event_order import EventOrder


def daily_earning(user, start_date, total_days):

    new_date = start_date
    earning_by_days = {}

    for i in range(0, total_days):
        new_date += timedelta(days=1)
        event = event = EventOrder.objects.filter(
            created_at__range=[start_date, new_date], event__user__id=user
        )
        total = event.aggregate(Sum("event__price"))
        start_date += timedelta(days=1)
        earning_by_days[str(start_date.strftime("%d-%m-%Y"))] = total[
            "event__price__sum"
        ]

    return earning_by_days
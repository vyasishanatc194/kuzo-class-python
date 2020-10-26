from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse


# ----------------------------------------------------------------------
# SubscriptionPlan Model
# ----------------------------------------------------------------------


class SubscriptionPlan(models.Model):

    """This model stores the data into Class table in db"""


    title = CharField(_("Title"), max_length=255,null=True, blank=True, unique=True)
    price = models.PositiveIntegerField(default=0, blank=True, null=True)
    number_of_credit = models.PositiveIntegerField(default=0, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

   
    class Meta:
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plan"

    def __str__(self):
        return "{0}".format(self.title)

from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse


# ----------------------------------------------------------------------
# Event Model
# ----------------------------------------------------------------------


class EventOrder(models.Model):

    """This model stores the data into Event Order table in db"""

   
    user = models.ForeignKey( 'core.user', on_delete=models.CASCADE, related_name="eventorder_user", null=True, blank=True)
    event = models.ForeignKey( 'core.event', on_delete=models.CASCADE, related_name="evntorder_order", null=True, blank=True)
    used_credit = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Used credit")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True,)

    class Meta:
        verbose_name = "Event Order"
        verbose_name_plural = "Event Order"

    def __str__(self):
        return "{0}".format(self.used_credit)

from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse


# ----------------------------------------------------------------------
# Event Model
# ----------------------------------------------------------------------


class Event(models.Model):

    """This model stores the data into Event table in db"""

    EVENT_TYPE = [
        ('class_qa','Class + Q&A (60min)'),
        ('meet_&_greet','Meet & Greet (20 min)')

    ]

    user = models.ForeignKey( 'core.user', on_delete=models.CASCADE, related_name="event_user", null=True, blank=True)
    event_types = models.CharField(max_length=222, blank=True, null=True, verbose_name="Event Types", choices=EVENT_TYPE)
    about = models.TextField(blank=True, null=True, verbose_name="About")
    event_class = models.ForeignKey( 'core.EventClass', on_delete=models.CASCADE, related_name="evnt_eventclass", null=True, blank=True)
    event_date_time = models.DateTimeField(blank=True, null=True, verbose_name="Event date & time")
    price = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Event Price")
    photo = models.FileField(upload_to="event", blank=True, null=True)
    number_of_participants = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="Event number of participants")
    remianing_spots = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="Event Remianing spots")
    credit_required = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="Event Credit required")
    session_lenght = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name="Session lenght"), 
    is_featured = models.BooleanField(default=False, verbose_name="Is featured") 
    is_popular = models.BooleanField(default=False, verbose_name="Is popular") 
    time_zone = models.CharField(max_length=222, blank=True, null=True, verbose_name="Event timezone"), 

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"


    def __str__(self):
        return "{0}".format(self.event_types)

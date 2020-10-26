from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse


# ----------------------------------------------------------------------
# Event Practice Audience QA Model
# ----------------------------------------------------------------------


class EventPracticeAudienceQA(models.Model):

    """This model stores the data into Event Order table in db"""

   
    event = models.ForeignKey( 'core.event', on_delete=models.CASCADE, related_name="evnt_qa", null=True, blank=True)
    question = models.CharField(max_length=222, blank=True, null=True, verbose_name="Question"), 
    answer =  models.TextField(blank=True, null=True, verbose_name="Answer")

    class Meta:
        verbose_name = "Event Practice Audience QA"
        verbose_name_plural = "Event Practice Audience QA"

    def __str__(self):
        return "{0}".format(self.question)

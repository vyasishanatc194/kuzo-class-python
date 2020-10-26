from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse


# ----------------------------------------------------------------------
# Class Model
# ----------------------------------------------------------------------


class UserProfile(models.Model):

    """This model stores the data into Class table in db"""

    user = models.ForeignKey( 'core.user', on_delete=models.CASCADE, related_name="user_profile", null=True, blank=True)
    influencer = models.ForeignKey( 'core.category', on_delete=models.CASCADE, related_name="user_catgeory", null=True, blank=True)
    subscription = models.ForeignKey( 'core.SubscriptionPlan', on_delete=models.CASCADE, related_name="user_subscription_plan", null=True, blank=True)
    photo = models.FileField(upload_to='photo', blank=True, null=True, verbose_name="Photo")
    video = models.FileField(upload_to='video', blank=True, null=True, verbose_name="Video")
    about = models.TextField(blank=True, null=True, verbose_name="About")
    credit = models.PositiveIntegerField(default=0, blank=True, null=True)
    follwer = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_popular = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True,)


    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Class"


    def __str__(self):
        return "{0}".format(self.name)

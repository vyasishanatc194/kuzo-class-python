from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    otp = models.PositiveIntegerField(null=True, blank=True)
    mobile = CharField(_("Mobile Number"), blank=True, max_length=255,null=True)
    sms_verification = models.BooleanField(default=False, verbose_name="sms verfication")
    sent_time = models.DateTimeField(default=timezone.now, null=False, blank=False, verbose_name='link send time')


    def get_absolute_url(self):
        return reverse("core:user-detail", kwargs={"username": self.username})
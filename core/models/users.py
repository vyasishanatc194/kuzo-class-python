from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import RegexValidator
# ------------------------------------------------------------------------
# User Model
# ------------------------------------------------------------------------


class User(AbstractUser):

    """This model stores the data into User table in db"""

    name = CharField(_("Name"), max_length=255)
    email = models.EmailField(max_length=255)
    about = models.TextField(blank=True, null=True)
    avatar = models.FileField(upload_to='avatar', default='sample.jpg', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True,)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True,)
    customer_id = CharField(_("Customer Id"), blank=True, max_length=255)
    firebase_token = models.TextField( _("Firebase Token"), blank=True, null=True)
 

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_absolute_url(self):
        return reverse("core:user-detail", kwargs={"name": self.name})

    def __str__(self):
        return "{0}".format(self.name)

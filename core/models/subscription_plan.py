from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.urls import reverse
from core.utils import MyStripe

# ----------------------------------------------------------------------
# SubscriptionPlan Model
# ----------------------------------------------------------------------

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

class SubscriptionPlan(models.Model):

    """This model stores the data into Class table in db"""


    title = CharField(_("Title"), max_length=255,null=True, blank=True, unique=True)
    price = models.PositiveIntegerField(default=0, blank=True, null=True)
    number_of_credit = models.PositiveIntegerField(default=0, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    stripe_plan_id = models.CharField(blank=True, null=True, max_length=222)
    stripe_product_id = models.CharField(blank=True, null=True, max_length=222)

   
    class Meta:
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plan"

    def __str__(self):
        return "{0}".format(self.title)

    def save(self, *args, **kwargs):

        stripe = MyStripe()
        product_obj = stripe.createProduct(self.title)
        plan_id = stripe.createPlan(int(self.price) * 100, 'month', product_obj['id'])
        self.stripe_plan_id = plan_id['id']
        self.stripe_product_id = product_obj['id']

        return super(SubscriptionPlan, self).save(*args, **kwargs)


@receiver(pre_delete, sender=SubscriptionPlan)
def delete_img_pre_delete_post(sender, instance, *args, **kwargs):
    stripe = MyStripe()
    stripe.deletePlan(instance.stripe_plan_id)
    stripe.deleteProduct(instance.stripe_product_id)
    return
    




from django.db import models

# ----------------------------------------------------------------------
# ContactUs Model
# ----------------------------------------------------------------------


class ContactUs(models.Model):

    """This model stores the data into Event table in db"""

    FAQ_TYPES = [
        ('general_faq','General_Faq'),
        ('event_faq','Event_Faq'),
        ('guideline_faq','Guideline_Faq'),

    ]

    email = models.EmailField(max_length=222, blank=True, null=True, verbose_name="Email"), 
    description =  models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True,)

    class Meta:
        verbose_name = "ContactUs"
        verbose_name_plural = "ContactUs"

    def __str__(self):
        return "{0}".format(self.email)

from django.db import models

# ----------------------------------------------------------------------
# Influencer Offer Model
# ----------------------------------------------------------------------


class InfluencerOffer(models.Model):

    """This model stores the data into Influencer Offer table in db"""

    user = models.ForeignKey(
        "core.user",
        on_delete=models.CASCADE,
        related_name="influenceroffer_user",
        null=True,
        blank=True,
    )
    offer = models.ForeignKey(
        "core.offer",
        on_delete=models.CASCADE,
        related_name="influenceroffer_offer",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Influencer Offer"
        verbose_name_plural = "Influencer Offer"

    def __str__(self):
        return "{0}".format(self.user.name)

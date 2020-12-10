from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models

# ----------------------------------------------------------------------
# Event Script
# ----------------------------------------------------------------------

class EventScript(models.Model):

    """This model stores the data into Event Script table in db"""

    event = models.ForeignKey(
        "core.event",
        on_delete=models.CASCADE,
        related_name="evnt_script",
        null=True,
        blank=True,
    )
    title = CharField(
        _("Title"),
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Event Script"
        verbose_name_plural = "Event Script"

    def __str__(self):
        return "{0}".format(self.title)

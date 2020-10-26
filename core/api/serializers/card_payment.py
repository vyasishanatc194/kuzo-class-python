from rest_framework import serializers

from core.models import Card
from core.utils import MyStripe

# -----------------------------------------------------------------------------
# Credit/ Debit Card serializers
# -----------------------------------------------------------------------------


class CardSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Card data into JSON
    """

    class Meta:
        model = Card
        fields = (
            "id",
            "user",
            "card_id",
            "customer_id",
            "brand",
            "exp_month",
            "exp_year",
            "last4",
            "name",
        )

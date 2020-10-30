from rest_framework import serializers

from core.models import InfluencerOffer

# -----------------------------------------------------------------------------
# Credit/ Debit Card serializers
# -----------------------------------------------------------------------------


class InfluencerOfferSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Card data into JSON
    """

    class Meta:
        model = InfluencerOffer
        fields = (
            "id",
            "user",
            "offer",
         
        
        )


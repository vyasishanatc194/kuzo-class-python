from rest_framework import serializers

from core.models import InfluencerTransferredMoney

# -----------------------------------------------------------------------------
# Influencer Transferred Money serializers
# -----------------------------------------------------------------------------


class InfluencerTransferredMoneySerializer(serializers.ModelSerializer):
    
    """
    Serializes the Banner data into JSON
    """

    class Meta:
        model = InfluencerTransferredMoney
        fields = ["id", 'user','amount', 'status', "transaction_id", "created_at"]
        
   
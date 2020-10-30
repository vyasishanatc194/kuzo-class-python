from rest_framework import serializers

from core.models import CreditOrder

# -----------------------------------------------------------------------------
# CreditOrder serializers
# -----------------------------------------------------------------------------


class CreditOrderSerializer(serializers.ModelSerializer):
    
    """
    Serializes the CreditOrder data into JSON
    """

    class Meta:
        model = CreditOrder
        fields = (
            "id",
            "user",
            "credit", 
            "amount", 
            "created_at", 
            "charge_id", 
            'order_status',

        )

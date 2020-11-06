from rest_framework import serializers

from core.models import EventOrder
from .event import EventListSerializer

# -----------------------------------------------------------------------------
# EventOrder serializers
# -----------------------------------------------------------------------------


class EventOrderSerializer(serializers.ModelSerializer):
    
    """
    Serializes the EventOrder data into JSON
    """

    class Meta:
        model = EventOrder
        fields = (
            "id",
            "user",
            "event", 
            "used_credit", 
            "created_at", 
            "charge_id", 
            'order_status',

        )



class EventOrderListSerializer(serializers.ModelSerializer):
    event=EventListSerializer()
    
    """
    Serializes the EventOrder data into JSON
    """

    class Meta:
        model = EventOrder
        fields = (
            "id",
            "user",
            "event", 
            "used_credit", 
            "created_at", 
            "charge_id", 
            'order_status',

        )


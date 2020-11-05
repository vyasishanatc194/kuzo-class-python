from rest_framework import serializers

from core.models import Event
from .event_class import EventClassSerializer
from core.api.serializers import UserUpdateDetailsSerializer

# -----------------------------------------------------------------------------
# Event serializers
# -----------------------------------------------------------------------------


class EventSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Event data into JSON
    """

    class Meta:
        model = Event
        fields = (
            "id",
            "user",
            "about",
            "event_types",
            "event_class",
            "event_date_time",
            "price",
            "photo",
            "number_of_participants",
            "credit_required",
            "session_lenght",

        
        )



class EventListSerializer(serializers.ModelSerializer):
    event_class = EventClassSerializer()
    user = UserUpdateDetailsSerializer()
    
    """
    Serializes the Event data into JSON
    """

    class Meta:
        model = Event
        fields = (
            "id",
            "user",
            "about",
            "event_types",
            "event_class",
            "event_date_time",
            "price",
            "photo",
            "number_of_participants",
            "credit_required",
            "session_lenght",

        
        )
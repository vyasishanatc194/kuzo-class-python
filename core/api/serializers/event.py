from rest_framework import serializers

from core.models import Event

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
            "event_types",
            "event_class",
            "event_date_time",
            "price",
            "photo",
            "number_of_participants",
            "credit_required",
            "session_lenght",

        
        )
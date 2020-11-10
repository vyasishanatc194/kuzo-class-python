from rest_framework import serializers

from core.models import Event
from .event_class import EventClassSerializer
from core.api.serializers import UserUpdateDetailsSerializer

import datetime, pytz

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
            "time_zone",

        
        )



class EventListSerializer(serializers.ModelSerializer):
    event_class = EventClassSerializer()
    user = UserUpdateDetailsSerializer()
    remaining_spots = serializers.SerializerMethodField('get_remaining_spots')
    timezone = serializers.SerializerMethodField('get_timezone')

    
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
            "is_featured",
            "is_popular",
            "created_at",
            "remaining_spots",
            "timezone",

        
        )

    def get_remaining_spots(self, event):
        remaining_spots = int(event.number_of_participants) - int(event.remianing_spots)
        return remaining_spots


    def get_timezone(self, event):
        if event.time_zone:
            timezone_code = datetime.datetime.now(tz=pytz.timezone(event.time_zone))
            data=timezone_code.strftime("%Z")
            return data
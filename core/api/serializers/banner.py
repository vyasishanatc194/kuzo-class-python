from rest_framework import serializers

from core.models import Banner

# -----------------------------------------------------------------------------
# Banners serializers
# -----------------------------------------------------------------------------


class BannerSerializer(serializers.ModelSerializer):
    
    """
    Serializes the Banner data into JSON
    """

    class Meta:
        model = Banner
        fields = (
            "id",
            "title",
            "description",
            "created_at",
        )

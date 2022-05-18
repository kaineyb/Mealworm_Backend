from rest_framework import serializers

from ..models import StoreAisle

# Sections Endpoint


class StoreAisleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAisle
        fields = ["id", "store", "aisle_number"]

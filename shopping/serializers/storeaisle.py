from email.policy import default

from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import StoreAisle
from .fields import (
    SectionsOfUserPrimaryKeyRelatedField,
    StoresOfUserPrimaryKeyRelatedField,
)

# Sections Endpoint


class StoreAisleSerializer(serializers.ModelSerializer):

    store = StoresOfUserPrimaryKeyRelatedField()

    class Meta:
        model = StoreAisle
        fields = ["id", "store", "aisle_number"]
        validators = [
            UniqueTogetherValidator(
                queryset=StoreAisle.objects.all(),
                fields=["store"],
                message="This Section already has an Aisle for that Store",
            )
        ]

    def create(self, request, *args, **kwargs):
        section = self.context["section_id"]
        with transaction.atomic():
            return StoreAisle.objects.create(section_id=section, **self.validated_data)


class UpdateStoreAisleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAisle
        fields = ["store", "aisle_number"]

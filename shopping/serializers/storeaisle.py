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

    @property
    def section(self):
        section_id = self.context["section_id"]
        return serializers.HiddenField(default=section_id)

    class Meta:
        model = StoreAisle
        fields = ["id", "store", "section", "aisle_number"]
        validators = [
            UniqueTogetherValidator(
                queryset=StoreAisle.objects.all(),
                fields=["store", "section"],
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

from django.db import transaction
from pytest import console_main
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import Store, StoreAisle
from ..serializers.section import SectionSerializer
from .fields import SectionsOfUserPrimaryKeyRelatedField

# Sections Endpoint


class StoreIdDefault:
    """
    May be applied as a `default=...` value on a serializer field.
    Returns the current store.
    """

    requires_context = True

    def __call__(self, serializer_field):

        store_id = int(serializer_field.context["stores_id"])

        return Store.objects.filter(pk=store_id).first()


class StoreAisleSerializer(serializers.ModelSerializer):
    section = SectionsOfUserPrimaryKeyRelatedField()
    store = serializers.HiddenField(default=StoreIdDefault())

    class Meta:
        model = StoreAisle
        fields = [
            "id",
            "aisle_number",
            "store",
            "section",
        ]

        validators = [
            UniqueTogetherValidator(
                queryset=StoreAisle.objects.all(),
                fields=["store", "section"],
                message="This Store already has an Aisle number assigned to that Section",
            )
        ]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            return StoreAisle.objects.create(**self.validated_data)


class UpdateStoreAisleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAisle
        fields = ["aisle_number"]

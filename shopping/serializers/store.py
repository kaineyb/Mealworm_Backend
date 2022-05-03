from django.db import transaction
from rest_framework import serializers

from ..models import Store, StoreAisle
from .fields import StoresOfUserPrimaryKeyRelatedField


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name"]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user_id = self.context["user_id"]
            return Store.objects.create(user_id=user_id, **self.validated_data)


class UpdateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name"]


class StoreAisleSerializer(serializers.ModelSerializer):

    store = StoresOfUserPrimaryKeyRelatedField()

    class Meta:
        model = StoreAisle
        fields = ["id", "store", "aisle_number"]

    def create(self, request, *args, **kwargs):
        section = self.context["section_id"]
        with transaction.atomic():
            return StoreAisle.objects.create(section_id=section, **self.validated_data)


class UpdateStoreAisleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAisle
        fields = ["store", "aisle_number"]

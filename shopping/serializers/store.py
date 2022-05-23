from django.db import transaction
from rest_framework import serializers

from ..models import Store
from ..serializers.store_aisle import StoreAisleSerializer


class StoreSerializer(serializers.ModelSerializer):
    aisles = StoreAisleSerializer(many=True, required=False)

    class Meta:
        model = Store
        fields = ["id", "name", "aisles"]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user_id = self.context["user_id"]
            return Store.objects.create(user_id=user_id, **self.validated_data)


class UpdateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name"]

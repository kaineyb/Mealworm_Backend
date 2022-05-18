from django.db import transaction
from rest_framework import serializers

from ..models import Section
from .storeaisle import StoreAisleSerializer

# Sections Endpoint


class SectionSerializer(serializers.ModelSerializer):

    storeaisle_set = StoreAisleSerializer(many=True, required=False)

    class Meta:
        model = Section
        fields = ["id", "name", "storeaisle_set"]

    def create(self, request, *args, **kwargs):
        user_id = self.context["user_id"]
        with transaction.atomic():
            return Section.objects.create(user_id=user_id, **self.validated_data)


class UpdateSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["name"]

from django.db import transaction
from rest_framework import serializers

from ..models import Section

# Sections Endpoint


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "name"]

    def create(self, request, *args, **kwargs):
        user_id = self.context["user_id"]
        with transaction.atomic():
            return Section.objects.create(user_id=user_id, **self.validated_data)




class UpdateSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["name"]

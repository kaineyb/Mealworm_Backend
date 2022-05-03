from django.db import transaction
from rest_framework import serializers

from ..models import Ingredient
from .fields import SectionsOfUserPrimaryKeyRelatedField

# Ingredients Endpoint


class IngredientSerializer(serializers.ModelSerializer):

    section = SectionsOfUserPrimaryKeyRelatedField(default=None)

    class Meta:
        model = Ingredient
        fields = [
            "id",
            "name",
            "section",
        ]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user_id = self.context["user_id"]
            return Ingredient.objects.create(user_id=user_id, **self.validated_data)


class UpdateIngredientSerializer(serializers.ModelSerializer):
    section = SectionsOfUserPrimaryKeyRelatedField(allow_null=True)

    class Meta:
        model = Ingredient
        fields = [
            "name",
            "section",
        ]

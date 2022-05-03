from django.db import transaction
from rest_framework import serializers

from ..models import Day, MealIngredient
from .fields import IngredientsOfUserPrimaryKeyRelatedField

# Meal Ingredients End Point


class MealIngredientSerializer(serializers.ModelSerializer):

    # ingredient = SimpleIngredientSerializer()

    class Meta:
        model = MealIngredient
        fields = [
            "id",
            "ingredient",
            "quantity",
            "unit",
        ]


class CreateMealIngredientSerializer(serializers.ModelSerializer):

    ingredient = IngredientsOfUserPrimaryKeyRelatedField()

    class Meta:
        model = MealIngredient
        fields = [
            "id",
            "ingredient",
            "quantity",
            "unit",
        ]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            meal_id = self.context["meals_pk"]
            return MealIngredient.objects.create(meal_id=meal_id, **self.validated_data)


class UpdateMealIngredientSerializer(serializers.ModelSerializer):
    """"""

    quantity = serializers.IntegerField()

    class Meta:
        model = MealIngredient
        fields = ["quantity", "unit"]

    def update(self, instance: Day, validated_data):

        quantity = self.validated_data["quantity"]
        unit = self.validated_data["unit"]

        MealIngredient.objects.filter(id=instance.pk).update(
            quantity=quantity, unit=unit
        )

        return MealIngredient.objects.filter(id=instance.pk).first()

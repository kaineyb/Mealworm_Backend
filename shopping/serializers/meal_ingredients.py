from audioop import mul
from typing import OrderedDict

from django.db import transaction
from rest_framework import serializers

from ..models import Meal, MealIngredient
from .fields import IngredientsOfUserPrimaryKeyRelatedField

# Meal Ingredients End Point


class MealIngredientListSerializer(serializers.ListSerializer):
    def update(self, instance: Meal, list_of_validated_data: list):
        print("MealIngredientListSerializer: I've been called!")

        print("MealIngredientListSerializer: validated_data", list_of_validated_data)

        validated_data: OrderedDict
        self.child: MealIngredientSerializer
        list_of_instances = []

        for validated_data in list_of_validated_data:

            id = validated_data.get("id")
            mi_instance: MealIngredient = MealIngredient.objects.filter(pk=id).first()

            if id and mi_instance:
                list_of_instances.append(self.child.update(mi_instance, validated_data))

            else:
                validated_data["meal_id"] = instance.pk

                print("mi_update_data with meal_id", validated_data)
                list_of_instances.append(self.child.create(validated_data))

        return list_of_instances


class MealIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealIngredient
        fields = [
            "id",
            "ingredient",
            "quantity",
            "unit",
        ]
        list_serializer_class = MealIngredientListSerializer


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

    ingredient = IngredientsOfUserPrimaryKeyRelatedField()
    quantity = serializers.IntegerField()

    class Meta:
        model = MealIngredient
        fields = ["ingredient", "quantity", "unit"]

    def update(self, instance, validated_data):

        MealIngredient.objects.filter(id=instance.pk).update(**validated_data)

        return MealIngredient.objects.filter(id=instance.pk).first()

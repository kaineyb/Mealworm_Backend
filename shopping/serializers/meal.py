from django.db import transaction
from rest_framework import serializers

from ..models import Meal
from .meal_ingredients import MealIngredientSerializer

# Meals Endpoint


class MealSerializer(serializers.ModelSerializer):

    meal_ingredients = MealIngredientSerializer(many=True, required=False)

    class Meta:
        model = Meal
        fields = ["id", "name", "meal_ingredients"]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():

            key = "meal_ingredients"

            meal_ingredients = (
                self.validated_data.pop(key) if self.validated_data.get(key) else False
            )

            if self.validated_data.get(key) == []:
                del self.validated_data[key]

            user_id = self.context["user_id"]
            new_meal: Meal = Meal.objects.create(user_id=user_id, **self.validated_data)

            if meal_ingredients:
                for instance in meal_ingredients:
                    new_meal.meal_ingredients.create(**instance)

            return new_meal

    def update(self, instance: Meal, validated_data: dict):

        nested_data_key = "meal_ingredients"

        nested_data = validated_data.get(nested_data_key)

        if nested_data:
            print("Got meal_ingredients in validated data")
            nested_serializer = self.fields[nested_data_key]
            nested_serializer.update(instance, validated_data[nested_data_key])

        if nested_data or nested_data == []:
            del validated_data[nested_data_key]

        Meal.objects.filter(pk=instance.pk).update(**validated_data)

        return Meal.objects.filter(pk=instance.pk).first()

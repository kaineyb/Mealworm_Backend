from django.db import transaction
from rest_framework import serializers

from ..models import Day, Meal
from .meal_ingredients import MealIngredientSerializer

# Meals Endpoint


class MealSerializer(serializers.ModelSerializer):
    meal_ingredients = MealIngredientSerializer(many=True)

    class Meta:
        model = Meal
        fields = ["id", "name", "meal_ingredients"]


class CreateMealSerializer(serializers.ModelSerializer):

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


class UpdateMealSerializer(serializers.ModelSerializer):

    meal_ingredients = MealIngredientSerializer(many=True, required=False)

    class Meta:
        model = Meal
        fields = ["name", "meal_ingredients"]

    def update(self, instance: Day, validated_data):

        name = self.validated_data["name"]
        print("validated_data", validated_data)
        Meal.objects.filter(id=instance.pk).update(name=name)
        return Meal.objects.filter(id=instance.pk).first()

from rest_framework import serializers
from ..models import Ingredient, Meal, Section, Store


class MealsOfUserPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    You can only associate Meals that belong to that User.
    """

    def get_queryset(self):
        user = self.context["user_id"]
        return Meal.objects.filter(user_id=user)


class StoresOfUserPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    You can only associate Stores that belong to that User.
    """

    def get_queryset(self):
        user = self.context["user_id"]
        return Store.objects.filter(user_id=user)


class IngredientsOfUserPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    You can only associate Ingredients that belong to that User.
    """

    def get_queryset(self):
        user = self.context["user_id"]
        return Ingredient.objects.filter(user_id=user)


class SectionsOfUserPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    You can only associate Sections that belong to that User.
    """

    def get_queryset(self):
        user = self.context["user_id"]
        queryset = Section.objects.filter(user_id=user)
        return queryset

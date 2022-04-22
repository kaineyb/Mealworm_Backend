from rest_framework import serializers
from ..models import Day, Ingredient, Meal, Store


class SimpleIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            "name",
        ]


class SimpleMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["id", "name"]

    def validate_id(self, value):
        """
        Is this used in this class?
        """
        user_id = self.context["user_id"]
        if not Meal.objects.filter(user_id=user_id).filter(pk=value).exists():
            raise serializers.ValidationError("No meal with the given ID was found.")
        return value


class NameOnlyMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["name"]

    def to_representation(self, obj):
        """
        Move fields from name to meal representation.
        ie {meal: "xyz"} from meal: {name: "xyz"}
        These means the below only grabs the name field and NOTHING ELSE.
        """

        representation = super().to_representation(obj)
        name_representation = representation.pop("name")
        return name_representation


class SimpleDaySerializer(serializers.ModelSerializer):
    meal = NameOnlyMealSerializer()

    class Meta:
        model = Day
        fields = ["id", "order", "meal"]

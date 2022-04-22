from statistics import mode
from rest_framework import serializers
from django.db import transaction
from ..models import (
    Day,
    Ingredient,
    Meal,
    Store,
    Section,
    Plan,
    MealIngredient,
    StoreAisle,
)
from .simple import (
    SimpleIngredientSerializer,
    SimpleMealSerializer,
    SimpleDaySerializer,
)
from .fields import (
    StoresOfUserPrimaryKeyRelatedField,
    MealsOfUserPrimaryKeyRelatedField,
    IngredientsOfUserPrimaryKeyRelatedField,
    SectionsOfUserPrimaryKeyRelatedField,
)

# Store Endpoint


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name"]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user_id = self.context["user_id"]
            return Store.objects.create(user_id=user_id, **self.validated_data)


class UpdateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name"]


class StoreAisleSerializer(serializers.ModelSerializer):

    store = StoresOfUserPrimaryKeyRelatedField()

    class Meta:
        model = StoreAisle
        fields = ["id", "store", "aisle_number"]

    def create(self, request, *args, **kwargs):
        section = self.context["section_id"]
        with transaction.atomic():
            return StoreAisle.objects.create(section_id=section, **self.validated_data)


class UpdateStoreAisleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAisle
        fields = ["store", "aisle_number"]


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


# Plans Endpoint


class UpdateDaySerializer(serializers.ModelSerializer):
    """Used for days/ PATCH"""

    class Meta:
        model = Day
        fields = ["order", "meal"]

    def validate_meal(self, value):
        """
        Stops users adding other users meals to their Plan Days.
        """
        user_id = self.context["user_id"]
        if not Meal.objects.filter(user_id=user_id).filter(id=value.id).exists():
            raise serializers.ValidationError("No meal with the given ID was found.")
        return value

    def update(self, instance: Day, validated_data):

        order = self.validated_data["order"]
        meal = self.validated_data["meal"]

        Day.objects.filter(id=instance.pk).update(order=order, meal=meal)

        # print(f"Updated Day:{instance.pk}, to order: {order} and meal_id {meal_id})")

        return Day.objects.filter(id=instance.pk).first()


class CreateDaySerializer(serializers.ModelSerializer):
    """Used for days/ POST"""

    meal = MealsOfUserPrimaryKeyRelatedField()

    class Meta:
        model = Day
        fields = ["order", "meal"]

    def validate_meal(self, value):
        """
        Makes sure that when you POST a meal it belongs to that user!
        """

        user_id = self.context["user_id"]
        if not Meal.objects.filter(user_id=user_id).filter(id=value.id).exists():
            raise serializers.ValidationError("No meal with the given ID was found.")

        return value

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            plan_id = int(self.context["plan_id"])
            order = self.validated_data["order"]
            meal = self.validated_data["meal"]

            print(f"{self.validated_data=}")

            return Day.objects.create(plan_id=plan_id, order=order, meal=meal)


class DayListSerializer(serializers.ListSerializer):
    pass


class DaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    meal = SimpleMealSerializer()

    class Meta:
        model = Day
        fields = ["id", "order", "meal"]
        list_serializer_class = DayListSerializer


class PlanSerializer(serializers.ModelSerializer):
    plan_days = DaySerializer(many=True)

    class Meta:
        model = Plan
        fields = ["id", "name", "start_day", "plan_days"]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user_id = self.context["user_id"]
            return Plan.objects.create(user_id=user_id, **self.validated_data)


class UpdatePlanSerializer(serializers.ModelSerializer):
    plan_days = DaySerializer(many=True)

    class Meta:
        model = Plan
        fields = ["name", "start_day", "plan_days"]

    def update(self, instance: Plan, validated_data):

        name = self.validated_data["name"]
        start_day = self.validated_data["start_day"]
        Plan.objects.filter(id=instance.pk).update(name=name, start_day=start_day)

        nested_serializer = self.fields["plan_days"]
        print(nested_serializer)
        nested_instance = instance.plan_days
        print(nested_instance)
        nested_data = validated_data.pop("plan_days")
        print(nested_data)
        # nested_serializer.update(nested_instance, nested_data)

        # print(plan_days)
        # print(validated_data["plan_days"])

        # Day.objects.filter()

        return Plan.objects.filter(id=instance.pk).first()


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


# Meal Ingredients End Point


class MealIngredientSerializer(serializers.ModelSerializer):

    ingredient = SimpleIngredientSerializer()

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


# Meals Endpoint


class MealSerializer(serializers.ModelSerializer):
    meal_ingredients = MealIngredientSerializer(many=True)

    class Meta:
        model = Meal
        fields = ["id", "name", "meal_ingredients"]


class CreateMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["id", "name"]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user_id = self.context["user_id"]
            meal = Meal.objects.create(user_id=user_id, **self.validated_data)
            return meal


class UpdateMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["name"]

    def update(self, instance: Day, validated_data):

        name = self.validated_data["name"]
        Meal.objects.filter(id=instance.pk).update(name=name)
        return Meal.objects.filter(id=instance.pk).first()

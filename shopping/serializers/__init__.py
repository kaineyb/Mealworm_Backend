from collections import OrderedDict
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
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        print("UPS Validate Called", data)
        return data

    def update(self, validated_data):

        print("Update DayListSerializer Fired")

        updated_day: OrderedDict
        self.child: DaySerializer
        list_of_instances = []

        for updated_day in validated_data:
            id = updated_day.get("id")
            order = updated_day.get("order")

            day_object: Day = Day.objects.filter(pk=id).first()

            meal = updated_day.get("meal")
            meal_object = Meal.objects.filter(pk=meal.id).first()

            data = {
                "order": order,
                "meal": meal,
            }

            # First check that this meal is for that user, and if it isn't we don't do anything.

            if not meal_object.user_id == self.context["user_id"]:
                continue

            # We check if this is an existing day or not.

            if id and day_object:
                # Update Day

                list_of_instances.append(self.child.update(day_object, data))
                print(
                    "Updating:",
                    updated_day,
                    "with data",
                    {"order": order, "meal": meal},
                )
            else:
                # New Day, create one with data
                print("day has not id, creating day")
                list_of_instances.append(self.child.create(data))

        return list_of_instances


class DaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Day
        fields = ["id", "order", "meal"]
        list_serializer_class = DayListSerializer

    def update(self, instance: Day, validated_data):
        print("Update DaySerializer Fired")
        instance.order = validated_data["order"]
        instance.meal = validated_data["meal"]
        instance.save()

        return instance


class PlanSerializer(serializers.ModelSerializer):
    plan_days = DaySerializer(many=True, required=False)

    class Meta:
        model = Plan
        fields = ["id", "name", "start_day", "plan_days"]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():

            list_of_days = (
                self.validated_data.pop("plan_days")
                if self.validated_data.get("plan_days")
                else False
            )

            print("self.validated_data", self.validated_data)

            user_id = self.context["user_id"]
            new_plan: Plan = Plan.objects.create(user_id=user_id, **self.validated_data)

            if list_of_days:

                for instance in list_of_days:
                    new_plan.plan_days.create(**instance)

                # Day.objects.bulk_create(instances)
                print("*" * 20)
                print("instances", list_of_days)
                print("*" * 20)

            # Check if plan_days key exists, could also be [] which is Falsey.

            return new_plan


class UpdatePlanSerializer(serializers.ModelSerializer):
    plan_days = DaySerializer(many=True, required=False)

    class Meta:
        model = Plan
        fields = ["name", "start_day", "plan_days"]

    def update(self, instance: Plan, validated_data: dict):

        print("initial_data", self.initial_data)
        # print("initial_data plan_days", self.initial_data["plan_days"])

        print("validators", self.get_validators())

        print("Update PlanSerializer Fired")
        print("*" * 20)
        print("ups: instance", instance)
        print("ups: validated_data", validated_data)
        print("*" * 20)

        instance.name = validated_data["name"]
        instance.start_day = validated_data["start_day"]

        if validated_data.get("plan_days"):
            print("Got plan_days in validated data")
            nested_serializer = self.fields["plan_days"]
            nested_serializer.update(validated_data["plan_days"])

        instance.save()

        return instance


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

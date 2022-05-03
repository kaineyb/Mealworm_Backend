from collections import OrderedDict

from django.db import transaction
from rest_framework import serializers

from ..models import Day, Meal
from .fields import MealsOfUserPrimaryKeyRelatedField


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
    def update(self, validated_data, plan_instance):

        print("*" * 20)
        print("DayListSerializer update()  fired")
        print("Received data:", validated_data)
        print("*" * 20)

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

            if not meal_object.user_id == self.context["user_id"]:
                continue

            if id and day_object:
                list_of_instances.append(self.child.update(day_object, data))

            else:
                data["plan"] = plan_instance
                list_of_instances.append(self.child.create(data))

        Day.objects.filter(plan_id=plan_instance.id).exclude(
            pk__in=[i.pk for i in list_of_instances]
        ).delete()

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

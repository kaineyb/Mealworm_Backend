from django.db import transaction
from rest_framework import serializers

from ..models import Plan
from .day import DaySerializer


class PlanSerializer(serializers.ModelSerializer):
    day_set = DaySerializer(many=True, required=False)

    class Meta:
        model = Plan
        fields = ["id", "name", "start_day", "day_set"]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():

            day_set = (
                self.validated_data.pop("day_set")
                if self.validated_data.get("day_set")
                else False
            )

            if self.validated_data.get("day_set") == []:
                del self.validated_data["day_set"]

            user_id = self.context["user_id"]
            new_plan: Plan = Plan.objects.create(user_id=user_id, **self.validated_data)

            if day_set:
                for instance in day_set:
                    new_plan.day_set.create(**instance)

            return new_plan


class UpdatePlanSerializer(serializers.ModelSerializer):
    day_set = DaySerializer(many=True, required=False)

    class Meta:
        model = Plan
        fields = ["name", "start_day", "day_set"]

    def update(self, instance: Plan, validated_data: dict):

        # print("*" * 20)
        # print("Update PlanSerializer Fired")
        # print("*" * 20)
        # print("initial_data", self.initial_data)
        # print("validators", self.get_validators())
        # print("instance", instance)
        # print("validated_data", validated_data)
        # print("Update PlanSerializer end")
        # print("*" * 20)

        instance.name = validated_data["name"]
        instance.start_day = validated_data["start_day"]

        if validated_data.get("day_set"):
            print("Got day_set in validated data")
            nested_serializer = self.fields["day_set"]
            nested_serializer.update(validated_data["day_set"], plan_instance=instance)

        instance.save()

        return instance
